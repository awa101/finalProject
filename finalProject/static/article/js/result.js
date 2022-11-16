const result = document.querySelector(".result");
const submitLink = document.querySelector(".search-box");
const inputLink = document.querySelector("input[name='article-link']");
const submitBtn = document.querySelector(".submit");
const resultClose = document.querySelector(".result button");
let score = 0;

function onSubmitLink(event) {
  event.preventDefault();

  $.ajax({
    url: "result",
    type: "GET",
    data: { inputLink: inputLink.value },
    datatype: "json",
    success: function (data) {
      result.classList.add("appear");
      return showResult(data);
    },
    error: function () {
      alert("링크를 다시 입력해 주세요");
    },
  });
}
function handleResultClose(event) {
  event.preventDefault();
  result.classList.remove("appear");
}

submitLink.addEventListener("submit", onSubmitLink);
resultClose.addEventListener("click", handleResultClose);

function showResult(news) {}
