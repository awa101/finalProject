const result = document.querySelector(".result");
const submitLink = document.querySelector(".search-box");
const inputLink = document.querySelector("input[name='article-link']");
const submitBtn = document.querySelector(".submit");
const resultClose = document.querySelector(".result button");
const score = document.querySelector(".score");

function showResult(news) {
  score.style.display = "flex";
  const scorePress = document.querySelector(".score-detail__press");
  const scoreReporter = document.querySelector(".score-detail__reporter");
  const scoreTime = document.querySelector(".score-detail__time");
  const scoreTitle = document.querySelector(".score-detail__title");
  const scoreImg = document.querySelector(".score-detail__right img");
  const scoreNum = document.querySelector(
    ".score-result__num span:first-child"
  );
  const scoreText = document.querySelector(".score-result__text");
  const resultImg = document.querySelector(".score-result img");
  console.log(news.id);
  scorePress.innerText = news.press;
  if (news.reporter !== "입력 ") {
    scoreReporter.innerText = news.reporter;
  }
  scoreTime.innerText = news.time;
  scoreTitle.innerText = news.title;
  if (news.img !== "video_news") {
    scoreImg.setAttribute("src", news.img);
  } else {
    scoreImg.closest(".score-detail__right").innerText = "사진이 없습니다.";
  }
  resultImg.setAttribute("src", `/static/media/article/wcimg${news.id}.png`);
  scoreNum.innerText = news.result;
  tempScore = evalResult(news.result);
  scoreText.innerText = tempScore.say;
  scoreNum.style.color = tempScore.color;
  document.querySelector(".score-result__num span:last-child").style.color =
    tempScore.color;
}

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

function onSubmitLink(event) {
  score.style.display = "none";
  result.classList.add("appear");
  event.preventDefault();
  $.ajax({
    url: "result",
    type: "GET",
    data: { inputLink: inputLink.value },
    datatype: "json",
    success: function (data) {
      return showResult(data);
    },
    error: function () {
      result.classList.remove("appear");
      alert("네이버 혹은 다음 을 통한 뉴스 링크를 넣어 주세요!");
    },
  });
}
function handleResultClose(event) {
  event.preventDefault();
  score.style.display = "none";
  result.classList.remove("appear");
}

submitLink.addEventListener("submit", onSubmitLink);
resultClose.addEventListener("click", handleResultClose);
