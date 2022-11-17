import { evalResult } from "./checkScore";
export function showResult(news) {
  const score = document.querySelector(".score");
  score.style.display = "flex";
  const scorePress = document.querySelector(".score-detail__press");
  const scoreReporter = document.querySelector(".score-detail__reporter");
  const scoreTime = document.querySelector(".score-detail__time");
  const scoreTitle = document.querySelector(".score-detail__title");
  const scoreImg = document.querySelector(".score-detail__right img");
  const scoreNum = document.querySelector(".score-result__num");
  const scoreText = document.querySelector(".score-result__text");
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
  scoreNum.innerText = news.result;
  scoreText.innerText = evalResult(news.result);
}
