window.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const canvas = document.getElementById('canvas');
  const addObjectBtn = document.getElementById('add-object-btn');
  const selectedObjectDropdown = document.querySelector('.dropdown-menu');
  let selectedElement = null;
  let objectId = 1;

  function makeDraggable(element) {
    let isDragging = false;
    let originalX = 0;
    let originalY = 0;
    let initialLeft = 0;
    let initialTop = 0;

    element.addEventListener('mousedown', (e) => {
      originalX = e.clientX;
      originalY = e.clientY;
      initialLeft = parseInt(element.style.left) || 0;
      initialTop = parseInt(element.style.top) || 0;

      isDragging = true;
      element.style.zIndex = '999';
    });

    document.addEventListener('mousemove', (e) => {
      if (isDragging) {
        const x = e.clientX - originalX;
        const y = e.clientY - originalY;
        element.style.left = initialLeft + x + 'px';
        element.style.top = initialTop + y + 'px';
      }
    });

    document.addEventListener('mouseup', () => {
      isDragging = false;
      element.style.zIndex = 'auto';
    });
  }

  function addObject() {
    const newObject = document.createElement('div');
    newObject.classList.add('draggable');
    newObject.style.left = '0px';
    newObject.style.top = '0px';
    newObject.textContent = '객체 ' + objectId;
    makeDraggable(newObject);
    canvas.appendChild(newObject);

    const dropdownItem = document.createElement('li');
    dropdownItem.textContent = `객체 ${objectId}`;
    dropdownItem.addEventListener('click', () => {
      selectedElement = newObject;
    });
    selectedObjectDropdown.appendChild(dropdownItem);

    objectId++;
  }

  addObjectBtn.addEventListener('click', addObject);
});
