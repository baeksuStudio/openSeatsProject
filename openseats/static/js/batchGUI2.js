window.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const canvas = document.getElementById('canvas');
  const addObjectBtn = document.getElementById('add-object-btn');
  const selectedObjectDropdown = document.querySelector('.dropdown-menu');
  let selectedElement = null;
  let offset = { x: 0, y: 0 };
  let objectId = 1;

  // 가이드 라인 요소 생성
  const guideLineX = document.createElement('div');
  guideLineX.classList.add('guide-line-x');
  const guideLineY = document.createElement('div');
  guideLineY.classList.add('guide-line-y');
  canvas.appendChild(guideLineX);
  canvas.appendChild(guideLineY);

  function makeDraggable(element) {
    let isDragging = false;
    let originalX = 0;
    let originalY = 0;
    let initialLeft = 0;
    let initialTop = 0;
    let isGuided = false; // 객체가 가이드 라인에 잡혔는지 여부를 저장하는 변수

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

        // 가이드 라인 위치 업데이트
        updateGuideLines(e.clientX, e.clientY);

        // 자석 효과 적용
        applyMagneticEffect(element, e.clientX, e.clientY);

        // 객체가 가이드 라인에 잡혔는지 체크
        if (isGuided) {
          const guideLineXPos = parseInt(guideLineX.style.left) || 0;
          const guideLineYPos = parseInt(guideLineY.style.top) || 0;

          // 현재 마우스 위치와 가이드 라인 사이의 거리 계산
          const distance = Math.sqrt(Math.pow(e.clientX - guideLineXPos, 2) + Math.pow(e.clientY - guideLineYPos, 2));

          // 일정 거리 이상 멀어지면 객체 놓아주기
          if (distance > 10) {
            isGuided = false;
            hideGuideLines();
          }
        }
      }
    });

    document.addEventListener('mouseup', () => {
      isDragging = false;
      element.style.zIndex = 'auto';

      // 가이드 라인 숨기기
      hideGuideLines();

      // 객체를 놓을 때 가이드 라인에 잡혔는지 여부 초기화
      isGuided = false;
    });
  }

  function updateGuideLines(mouseX, mouseY) {
    const objects = Array.from(document.getElementsByClassName('draggable'));

    const closestX = getClosestGuideLine(objects, mouseX, 'x');
    const closestY = getClosestGuideLine(objects, mouseY, 'y');

    // 가이드 라인 위치 설정
    if (closestX !== null) {
      guideLineX.style.display = 'block';
      guideLineX.style.left = closestX + 'px';
    } else {
      guideLineX.style.display = 'none';
    }

    if (closestY !== null) {
      guideLineY.style.display = 'block';
      guideLineY.style.top = closestY + 'px';
    } else {
      guideLineY.style.display = 'none';
    }
  }

  function getClosestGuideLine(objects, coordinate, axis) {
    let closest = null;

    objects.forEach((obj) => {
      const objRect = obj.getBoundingClientRect();

      let linePosition;
      let elementPosition;

      if (axis === 'x') {
        linePosition = objRect.left + objRect.width / 2;
        elementPosition = coordinate;
      } else if (axis === 'y') {
        linePosition = objRect.top + objRect.height / 2;
        elementPosition = coordinate;
      }

      if (closest === null || Math.abs(linePosition - elementPosition) < Math.abs(closest - elementPosition)) {
        closest = linePosition;
      }
    });

    return closest;
  }

  function applyMagneticEffect(element, mouseX, mouseY) {
    const guideLineXPos = parseInt(guideLineX.style.left) || 0;
    const guideLineYPos = parseInt(guideLineY.style.top) || 0;

    const threshold = 25; // 가이드 라인과 객체 사이의 거리 임계값

    // X 축 자석 효과 적용
    if (Math.abs(guideLineXPos - mouseX) <= threshold) {
      element.style.left = guideLineXPos - element.offsetWidth / 2 + 'px';

      // 가이드 라인에 잡혔음을 표시
      isGuided = true;
    }

    // Y 축 자석 효과 적용
    if (Math.abs(guideLineYPos - mouseY) <= threshold) {
      element.style.top = guideLineYPos - element.offsetHeight / 2 + 'px';

      // 가이드 라인에 잡혔음을 표시
      isGuided = true;
    }
  }

  function hideGuideLines() {
    guideLineX.style.display = 'none';
    guideLineY.style.display = 'none';
  }

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
      selectedElement = newObject;
    });
    selectedObjectDropdown.appendChild(dropdownItem);

    objectId++;
  }

  addObjectBtn.addEventListener('click', addObject);
});
