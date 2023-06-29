// 페이지 로드 시 실행되는 함수
window.onload = function() {
    // 모든 섹션 숨기기
    var sections = document.getElementsByClassName('section');
    for (var i = 0; i < sections.length; i++) {
        sections[i].style.display = 'none';
    }

    // create-section 섹션 보이기
    document.getElementById('create-section').style.display = 'block';

    var checkbox = document.getElementById('preview-on/off');
    checkbox.addEventListener('change', togglePreview);

    // 체크박스를 체크되지 않은 상태로 설정
    checkbox.checked = false;
    togglePreview(); // 초기에 프리뷰 숨김 처리

    //사이드 바 on/off 객체 생성
    var sidebarBtn = document.getElementById('sidebar-on-off');
    sidebarBtn.addEventListener('click', toggleSidebar);
  
};

// 선택된 값에 따라 섹션을 표시하거나 숨기는 함수
function showSection(sectionId) {
    // 모든 섹션 숨기기
    var sections = document.getElementsByClassName("section");
    for (var i = 0; i < sections.length; i++) {
      sections[i].style.display = "none";
    }
  
    // 선택된 섹션 표시
    var section = document.getElementById(sectionId);
    if (section) {
      section.style.display = "block";
    }
  }
  
  // 라디오 버튼 변경 시 이벤트 처리
  var radioButtons = document.getElementsByName("btnradio");
  for (var i = 0; i < radioButtons.length; i++) {
    radioButtons[i].addEventListener("change", function() {
      var selectedOption = document.querySelector('input[name="btnradio"]:checked').id;
      var sectionId = "";
  
      // 선택된 값에 따라 표시할 섹션 ID 설정
      switch (selectedOption) {
        case "btnradio1":
          sectionId = "create-section";
          break;
        case "btnradio2":
          sectionId = "edit-section";
          break;
        case "btnradio3":
          sectionId = "settings-section";
          break;
      }
  
      // 선택된 값에 따라 섹션 표시
      showSection(sectionId);
    });
  }

// 체크박스 변경 이벤트 핸들러
function togglePreview() {
    var preview = document.getElementById('preview');
    var checkbox = document.getElementById('preview-on/off');

    // 체크박스 상태에 따라 프리뷰 보이기/숨기기
    if (checkbox.checked) {
        preview.style.display = 'block';
    } else {
        preview.style.display = 'none';
    }
}
function toggleSidebar() {
    var sideSpace = document.getElementById('side-space');
    var workSpace = document.getElementById('work-space');

    if (sideSpace.style.display === 'none') {
      sideSpace.style.display = 'block';
      workSpace.classList.remove('col-md-12');
      workSpace.classList.add('col-md-10');
    } else {
      sideSpace.style.display = 'none';
      workSpace.classList.remove('col-md-10');
      workSpace.classList.add('col-md-12');
    }
  
}
