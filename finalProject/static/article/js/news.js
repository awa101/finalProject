var requestURL = "../data.json";
var request = new XMLHttpRequest();
const topTen = document.querySelector("h1");

request.open("GET", requestURL);
request.responseType = "json";

request.send();
const news = request.response;

request.onload = function () {
  var news = request.response;
  newsTitle(news);
};

function newsTitle(jsonObj) {
  console.log(jsonObj[4]["title"]);
  console.log(jsonObj[4]["category"]);
  console.log(jsonObj[4]["thumbnail"]);
  console.log(jsonObj[4]["logo"]);
  console.log(jsonObj[4]["title"]);
}
