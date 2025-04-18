// Dark mode functionality
document.addEventListener('DOMContentLoaded', function() {
  // Get the theme toggle button and body element
  const themeToggle = document.querySelector('.theme-toggle');
  const body = document.body;

  // Check for saved user preference, first in localStorage, then in system preferences
  const darkMode = localStorage.getItem('darkMode') || 
                  window.matchMedia('(prefers-color-scheme: dark)').matches;

  // Set initial theme
  if (darkMode === 'true' || darkMode === true) {
      body.classList.add('dark-mode');
      updateThemeIcon(true);
  }

  // Toggle theme on button click
  themeToggle.addEventListener('click', () => {
      body.classList.toggle('dark-mode');
      
      // Save user preference
      localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
      
      // Update icon
      updateThemeIcon(body.classList.contains('dark-mode'));
  });

  // Function to update the theme icon
  function updateThemeIcon(isDark) {
      const icon = themeToggle.querySelector('i');
      const text = themeToggle.querySelector('span');
      
      if (isDark) {
          icon.className = 'fas fa-sun';
          text.textContent = 'Light Mode';
      } else {
          icon.className = 'fas fa-moon';
          text.textContent = 'Dark Mode';
      }
  }
  
  // Task Modal Functionality
  const taskModal = document.getElementById('taskModal');
  const addTaskBtn = document.querySelector('.header-actions .btn.primary');
  
  if (addTaskBtn) {
    addTaskBtn.addEventListener('click', () => {
      // Reset the form
      document.getElementById('modalTitle').textContent = 'Create New Task';
      document.getElementById('taskId').value = '';
      document.getElementById('title').value = '';
      document.getElementById('priority').value = 'medium';
      document.getElementById('category').value = 'other';
      document.getElementById('due_date').value = '';
      document.getElementById('tags').value = '';
      
      // Update form action
      document.getElementById('taskForm').action = "/add-task/";
      
      // Update submit button text
      document.getElementById('submitButton').textContent = 'Create Task';
      
      // Show the modal
      taskModal.classList.add('show');
    });
  }
  
  // Set up edit task functionality
  const editButtons = document.querySelectorAll('.task-actions .btn-icon:nth-child(2)');
  editButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const taskCard = this.closest('.task-card');
      const taskId = this.getAttribute('href').split('/').pop();
      const taskTitle = taskCard.querySelector('h3').textContent;
      const taskPriority = taskCard.querySelector('.priority').textContent.trim();
      const taskCategory = taskCard.querySelector('.category').textContent.trim();
      const taskDueDate = taskCard.querySelector('.due-date').textContent.trim().split(' ').pop();
      
      // Get tags if they exist
      let taskTags = '';
      const tagsContainer = taskCard.querySelector('.task-tags');
      if (tagsContainer) {
        const tags = tagsContainer.querySelectorAll('.tag');
        taskTags = Array.from(tags).map(tag => tag.textContent.trim()).join(', ');
      }
      
      // Populate the form
      document.getElementById('modalTitle').textContent = 'Edit Task';
      document.getElementById('taskId').value = taskId;
      document.getElementById('title').value = taskTitle;
      document.getElementById('priority').value = taskPriority.toLowerCase();
      document.getElementById('category').value = taskCategory.toLowerCase();
      document.getElementById('due_date').value = taskDueDate;
      document.getElementById('tags').value = taskTags;
      
      // Update form action
      document.getElementById('taskForm').action = `/edit-task/${taskId}/`;
      
      // Update submit button text
      document.getElementById('submitButton').textContent = 'Save Changes';
      
      // Show the modal
      taskModal.classList.add('show');
    });
  });
  
  // Close modal when clicking outside
  window.addEventListener('click', (e) => {
    if (e.target === taskModal) {
      closeTaskModal();
    }
  });
  
  // Search Functionality
  const searchInput = document.getElementById('searchInput');
  const taskCards = document.querySelectorAll('.task-card');
  
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const searchTerm = searchInput.value.toLowerCase();
      
      taskCards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const category = card.querySelector('.category').textContent.toLowerCase();
        const tags = card.querySelectorAll('.tag');
        let tagText = '';
        
        tags.forEach(tag => {
          tagText += tag.textContent.toLowerCase() + ' ';
        });
        
        if (title.includes(searchTerm) || category.includes(searchTerm) || tagText.includes(searchTerm)) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }
});

// Function to close the task modal
function closeTaskModal() {
  document.getElementById('taskModal').classList.remove('show');
}