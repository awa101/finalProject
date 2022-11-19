const openModalButtons = document.querySelectorAll("[data-modal-target]");
const closeModalButtons = document.querySelectorAll("[data-close-button]");
const overlay = document.getElementById("overlay");
const modalScore = document.querySelectorAll("[data-result]");

function evalResult(score) {
  if (score > 79) {
    return { say: "정확합니다!", color: "#58f26c" };
  } else if (80 > score && score > 59) {
    return { say: "맞는것같습니다!", color: "#33d1e0" };
  } else if (60 > score && score > 49) {
    return { say: "긴가민가 합니다@", color: "#ecf470" };
  } else if (50 > score && score > 19) {
    return { say: "아닐확률 높아요", color: "#faa602" };
  } else {
    return { say: "못믿음", color: "#fa3a01" };
  }
}
function paintModal() {
  modalScore.forEach((score) => {
    const temp = evalResult(score.querySelector(".modal-num").innerText);
    score.querySelector(".modal-num").style.color = temp.color;
    score.querySelector(".modal-text").innerText = temp.say;
  });
}

openModalButtons.forEach((li) => {
  li.addEventListener("click", () => {
    const news = document.querySelector(li.dataset.modalTarget);
    openModal(news);
  });
});

closeModalButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const modal = button.closest(".modal");
    closeModal(modal);
  });
});

function openModal(news) {
  if (news == null) return;
  news.classList.add("active");
  overlay.classList.add("active");
}

function closeModal(modal) {
  if (modal == null) return;
  modal.classList.remove("active");
  overlay.classList.remove("active");
}
paintModal();
