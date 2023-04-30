// password input과 confirmPassword input, registerBtn을 가져옴
var passwordInput = document.getElementById("password1");
var confirmPasswordInput = document.getElementById("password2");
var registerBtn = document.getElementById("registerBtn");

// 비밀번호를 검사하는 함수
function checkPassword() {
// 비밀번호와 확인 비밀번호가 일치하면 is-invalid 클래스를 제거하고 registerBtn을 활성화 함
if (passwordInput.value === confirmPasswordInput.value) {
    confirmPasswordInput.classList.remove("is-invalid");
    registerBtn.disabled = false;
}
// 비밀번호와 확인 비밀번호가 일치하지 않으면 is-invalid 클래스를 추가하고 registerBtn을 비활성화 함
else {
    confirmPasswordInput.classList.add("is-invalid");
    registerBtn.disabled = true;
}
}

// passwordInput과 confirmPasswordInput의 input 이벤트에 checkPassword 함수를 등록함
passwordInput.addEventListener("input", checkPassword);
confirmPasswordInput.addEventListener("input", checkPassword);

