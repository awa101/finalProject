const result = document.querySelector(".result");
const submitLink = document.querySelector(".search-box");
const submitBtn = document.querySelector(".submit");
const resultClose = document.querySelector(".result button");

function onSubmitLink(event) {
  event.preventDefault();
  result.classList.add("appear");
  console.log(12);
}
function handleResultClose(event) {
  event.preventDefault();
  console.log(12);
  result.classList.remove("appear");
}

submitLink.addEventListener("submit", onSubmitLink);
resultClose.addEventListener("click", handleResultClose);
