window.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const canvas = document.getElementById('canvas');
  const addObjectBtn = document.getElementById('add-object-btn');
  const selectedObjectDropdown = document.querySelector('.dropdown-menu');
  let selectedElement = null;
  let offset = { x: 0, y: 0 };
  let objectId = 1;

  // 객체를 드래그 가능하게 만들어주는 함수
  function makeDraggable(element) {
    let isDragging = false;
    let originalX = 0;
    let originalY = 0;
    let initialLeft = 0;
    let initialTop = 0;

    // 마우스 다운 이벤트 처리
    element.addEventListener('mousedown', (e) => {
      originalX = e.clientX;
      originalY = e.clientY;
      initialLeft = parseInt(element.style.left) || 0;
      initialTop = parseInt(element.style.top) || 0;

      isDragging = true;
      element.style.zIndex = '999';
    });

    // 마우스 이동 이벤트 처리
    document.addEventListener('mousemove', (e) => {
      if (isDragging) {
        const x = e.clientX - originalX;
        const y = e.clientY - originalY;
        element.style.left = initialLeft + x + 'px';
        element.style.top = initialTop + y + 'px';
      }
    });

    // 마우스 업 이벤트 처리
    document.addEventListener('mouseup', () => {
      isDragging = false;
      element.style.zIndex = 'auto';
    });
  }

  // 객체를 생성하고 선택할 수 있는 함수
  function addObject() {
    const newObject = document.createElement('div');
    newObject.classList.add('draggable');
    newObject.style.left = '0px';
    newObject.style.top = '0px';
    newObject.innerText = '객체 ' + objectId;
    makeDraggable(newObject);
    canvas.appendChild(newObject);

    const dropdownItem = document.createElement('li');
    dropdownItem.innerHTML = `<a class="dropdown-item" href="#">객체 ${objectId}</a>`;
    dropdownItem.addEventListener('click', () => {
      selectedObjectDropdown.previousElementSibling.innerText = '선택된 객체: ' + dropdownItem.innerText;
      selectedElement = newObject;
    });
    selectedObjectDropdown.appendChild(dropdownItem);

    objectId++;
  }

  // 객체 추가 버튼 클릭 시 객체 생성
  addObjectBtn.addEventListener('click', () => {
    addObject();
  });

  // canvas에 드롭된 객체를 생성
  canvas.addEventListener('mousedown', (e) => {
    if (selectedElement !== null) {
      const clone = selectedElement.cloneNode(true);
      clone.style.position = 'absolute';
      clone.style.left = e.pageX - canvas.offsetLeft - offset.x + 'px';
      clone.style.top = e.pageY - canvas.offsetTop - offset.y + 'px';
      makeDraggable(clone);
      canvas.appendChild(clone);
      selectedElement = null;
    }
  });

  // grid의 아이템들에 드래그 기능 추가
  const gridItems = document.getElementsByClassName('grid-item');
  for (const item of gridItems) {
    makeDraggable(item);
  }
});