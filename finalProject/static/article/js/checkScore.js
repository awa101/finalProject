export function evalResult(score) {
  if (score > 79) {
    return "정확합니다!";
  } else if (80 > score > 59) {
    return "맞는것같습니다!";
  } else if (60 > score > 49) {
    return "긴가민가 합니다@";
  } else if (50 > score > 19) {
    return "아닐확률 높아요";
  } else {
    return "못믿음";
  }
}
