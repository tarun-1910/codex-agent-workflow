(() => {
  'use strict';

  const STORAGE_KEY = 'taskflow.tasks.v1';
  const THEME_KEY = 'taskflow.theme';
  const statuses = { todo: 'To do', 'in-progress': 'In progress', done: 'Completed' };
  const priorities = { low: 1, medium: 2, high: 3 };
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const els = {
    list: $('#task-list'), empty: $('#empty-state'), emptyTitle: $('#empty-title'), emptyDescription: $('#empty-description'),
    template: $('#task-template'), dialog: $('#task-dialog'), form: $('#task-form'), title: $('#task-title'),
    description: $('#task-description'), status: $('#task-status'), priority: $('#task-priority'), date: $('#task-due-date'),
    id: $('#task-id'), save: $('#save-task-button'), titleError: $('#title-error'), dateError: $('#date-error'),
    search: $('#search-input'), sort: $('#sort-select'), toast: $('#toast'),
    total: $('#total-stat'), progress: $('#progress-stat'), completed: $('#completed-stat'), allCount: $('#all-count'),
    filterAllCount: $('#filter-all-count'), viewLabel: $('#view-label'), todayLabel: $('#today-label')
  };

  let tasks = readTasks();
  let viewFilter = 'all';
  let statusFilter = 'all';
  let toastTimer;

  function readTasks() {
    try {
      const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      if (!Array.isArray(stored)) return [];
      return stored.filter(task => task && typeof task.id === 'string' && typeof task.title === 'string').map(task => ({
        id: task.id, title: task.title, description: typeof task.description === 'string' ? task.description : '',
        status: statuses[task.status] ? task.status : 'todo', priority: priorities[task.priority] ? task.priority : 'medium',
        dueDate: typeof task.dueDate === 'string' ? task.dueDate : '', createdAt: Number(task.createdAt) || Date.now(), updatedAt: Number(task.updatedAt) || Number(task.createdAt) || Date.now()
      }));
    } catch (error) {
      return [];
    }
  }

  function persist() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
      return true;
    } catch (error) {
      showToast('Could not save tasks. Check available browser storage.');
      return false;
    }
  }

  function showToast(message) {
    els.toast.textContent = message;
    els.toast.classList.add('show');
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => els.toast.classList.remove('show'), 2600);
  }

  function localDateString(date = new Date()) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  function formatDate(value) {
    if (!value) return '';
    const [year, month, day] = value.split('-').map(Number);
    const date = new Date(year, month - 1, day);
    return new Intl.DateTimeFormat(undefined, { month: 'short', day: 'numeric', year: 'numeric' }).format(date);
  }

  function visibleTasks() {
    const query = els.search.value.trim().toLowerCase();
    const today = localDateString();
    const result = tasks.filter(task => {
      if (viewFilter === 'today' && task.dueDate !== today && task.status !== 'done') return false;
      if (viewFilter === 'upcoming' && (!task.dueDate || task.dueDate <= today || task.status === 'done')) return false;
      if (viewFilter === 'completed' && task.status !== 'done') return false;
      if (statusFilter !== 'all' && task.status !== statusFilter) return false;
      return !query || `${task.title} ${task.description} ${task.priority} ${statuses[task.status]}`.toLowerCase().includes(query);
    });
    const mode = els.sort.value;
    result.sort((a, b) => {
      if (mode === 'due') return (a.dueDate || '9999-12-31').localeCompare(b.dueDate || '9999-12-31') || b.createdAt - a.createdAt;
      if (mode === 'priority') return priorities[b.priority] - priorities[a.priority] || b.createdAt - a.createdAt;
      return b.createdAt - a.createdAt;
    });
    return result;
  }

  function renderStats() {
    const completed = tasks.filter(task => task.status === 'done').length;
    els.total.textContent = tasks.length;
    els.progress.textContent = tasks.filter(task => task.status === 'in-progress').length;
    els.completed.textContent = completed;
    els.allCount.textContent = tasks.length;
    els.filterAllCount.textContent = tasks.length;
  }

  function render() {
    renderStats();
    els.list.replaceChildren();
    const shown = visibleTasks();
    for (const task of shown) {
      const row = els.template.content.firstElementChild.cloneNode(true);
      row.dataset.id = task.id;
      if (task.status === 'done') row.classList.add('is-done');
      $('.task-title', row).textContent = task.title;
      $('.task-description', row).textContent = task.description;
      const priority = $('.priority-badge', row);
      priority.textContent = `${task.priority} priority`;
      priority.classList.add(task.priority);
      const status = $('.status-badge', row);
      status.textContent = statuses[task.status];
      status.classList.add(`status-${task.status}`);
      const date = $('.task-date', row);
      if (task.dueDate) {
        date.textContent = `Due ${formatDate(task.dueDate)}`;
        if (task.dueDate < localDateString() && task.status !== 'done') date.classList.add('overdue');
      }
      $('.task-updated', row).textContent = `Updated ${new Intl.DateTimeFormat(undefined, { month: 'short', day: 'numeric' }).format(task.updatedAt)}`;
      const toggle = $('.status-toggle', row);
      toggle.setAttribute('aria-label', task.status === 'done' ? 'Mark task to do' : 'Mark task complete');
      toggle.addEventListener('click', () => cycleStatus(task.id));
      $('.edit-action', row).addEventListener('click', () => openEditor(task));
      $('.delete-action', row).addEventListener('click', () => deleteTask(task.id));
      els.list.append(row);
    }

    const hasTasks = shown.length > 0;
    els.empty.hidden = hasTasks;
    els.list.hidden = !hasTasks;
    if (!hasTasks) {
      const hasAnyTasks = tasks.length > 0;
      els.emptyTitle.textContent = hasAnyTasks ? 'No tasks match this view' : 'Nothing on your list yet';
      els.emptyDescription.textContent = hasAnyTasks ? 'Try another filter or search term.' : 'Add a task to turn your plans into progress.';
      $('#empty-add-button').hidden = hasAnyTasks;
    }
  }

  function setView(filter) {
    viewFilter = filter;
    statusFilter = 'all';
    $$('.nav-item').forEach(button => button.classList.toggle('active', button.dataset.filter === filter));
    $$('.filter-chip').forEach(button => button.classList.toggle('active', button.dataset.status === 'all'));
    const label = { all: 'All tasks', today: 'Today', upcoming: 'Upcoming', completed: 'Completed' }[filter] || 'All tasks';
    els.viewLabel.textContent = label;
    $('#task-list-title').textContent = filter === 'all' ? 'Your tasks' : label;
    render();
  }

  function setStatusFilter(filter) {
    statusFilter = filter;
    $$('.filter-chip').forEach(button => button.classList.toggle('active', button.dataset.status === filter));
    render();
  }

  function clearValidation() {
    els.titleError.textContent = '';
    els.dateError.textContent = '';
    els.title.classList.remove('input-invalid');
    els.date.classList.remove('input-invalid');
  }

  function validateForm() {
    clearValidation();
    let valid = true;
    if (!els.title.value.trim()) {
      els.titleError.textContent = 'Enter a task name.';
      els.title.classList.add('input-invalid');
      valid = false;
    }
    if (els.date.value) {
      const parsed = new Date(`${els.date.value}T00:00:00`);
      if (Number.isNaN(parsed.getTime()) || localDateString(parsed) !== els.date.value) {
        els.dateError.textContent = 'Enter a valid due date.';
        els.date.classList.add('input-invalid');
        valid = false;
      }
    }
    if (!valid) (els.title.classList.contains('input-invalid') ? els.title : els.date).focus();
    return valid;
  }

  function openCreate() {
    els.form.reset();
    els.id.value = '';
    els.status.value = 'todo';
    els.priority.value = 'medium';
    $('#dialog-title').textContent = 'Create a task';
    els.save.textContent = 'Create task';
    clearValidation();
    els.dialog.showModal();
    els.title.focus();
  }

  function openEditor(task) {
    els.form.reset();
    els.id.value = task.id;
    els.title.value = task.title;
    els.description.value = task.description;
    els.status.value = task.status;
    els.priority.value = task.priority;
    els.date.value = task.dueDate;
    $('#dialog-title').textContent = 'Edit task';
    els.save.textContent = 'Save changes';
    clearValidation();
    els.dialog.showModal();
    els.title.focus();
  }

  function submitForm(event) {
    event.preventDefault();
    if (!validateForm()) return;
    const now = Date.now();
    const existing = tasks.find(task => task.id === els.id.value);
    const record = {
      id: existing ? existing.id : (window.crypto && crypto.randomUUID ? crypto.randomUUID() : `${now}-${Math.random().toString(16).slice(2)}`),
      title: els.title.value.trim(), description: els.description.value.trim(), status: els.status.value,
      priority: els.priority.value, dueDate: els.date.value,
      createdAt: existing ? existing.createdAt : now, updatedAt: now
    };
    const previous = tasks;
    tasks = existing ? tasks.map(task => task.id === existing.id ? record : task) : [record, ...tasks];
    if (!persist()) { tasks = previous; return; }
    els.dialog.close();
    render();
    showToast(existing ? 'Task updated.' : 'Task created.');
  }

  function cycleStatus(id) {
    const transitions = { todo: 'in-progress', 'in-progress': 'done', done: 'todo' };
    const previous = tasks;
    tasks = tasks.map(task => task.id === id ? { ...task, status: transitions[task.status], updatedAt: Date.now() } : task);
    if (!persist()) { tasks = previous; return; }
    render();
    const updated = tasks.find(task => task.id === id);
    showToast(`Status changed to ${statuses[updated.status].toLowerCase()}.`);
  }

  function deleteTask(id) {
    const task = tasks.find(item => item.id === id);
    if (!task || !window.confirm(`Delete “${task.title}”? This cannot be undone.`)) return;
    const previous = tasks;
    tasks = tasks.filter(item => item.id !== id);
    if (!persist()) { tasks = previous; return; }
    render();
    showToast('Task deleted.');
  }

  $$('.nav-item').forEach(button => button.addEventListener('click', () => setView(button.dataset.filter)));
  $$('.filter-chip').forEach(button => button.addEventListener('click', () => setStatusFilter(button.dataset.status)));
  $('#add-task-button').addEventListener('click', openCreate);
  $('#empty-add-button').addEventListener('click', openCreate);
  $('#close-dialog').addEventListener('click', () => els.dialog.close());
  $('#cancel-dialog').addEventListener('click', () => els.dialog.close());
  els.form.addEventListener('submit', submitForm);
  els.title.addEventListener('input', () => { if (els.title.value.trim()) { els.titleError.textContent = ''; els.title.classList.remove('input-invalid'); } });
  els.date.addEventListener('change', () => { els.dateError.textContent = ''; els.date.classList.remove('input-invalid'); });
  els.search.addEventListener('input', render);
  els.sort.addEventListener('change', render);
  els.dialog.addEventListener('click', event => { if (event.target === els.dialog) els.dialog.close(); });
  $('#theme-button').addEventListener('click', () => {
    document.body.classList.toggle('dark');
    try { localStorage.setItem(THEME_KEY, document.body.classList.contains('dark') ? 'dark' : 'light'); } catch (error) { /* Theme still works for this session. */ }
  });
  try { if (localStorage.getItem(THEME_KEY) === 'dark') document.body.classList.add('dark'); } catch (error) { /* Use the default theme when storage is unavailable. */ }
  els.todayLabel.textContent = new Intl.DateTimeFormat(undefined, { weekday: 'short', month: 'short', day: 'numeric' }).format(new Date());
  render();
})();