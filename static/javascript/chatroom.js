document.addEventListener("DOMContentLoaded", () => {
  setInterval(function () {
    let request = new XMLHttpRequest();
    const path = window.location.pathname.split("/").filter(Boolean).pop();
    request.open("GET", "/getMessages/" + path, true);
    request.onload = function () {
      let response = JSON.parse(this.response);
      var messageList = "";
      for (let i in response) {
        let listOfMessages = response[i];
        for (let j in listOfMessages) {
          let username = '<div class="messageUsername">' + listOfMessages[j].username + "</div>";
          if (listOfMessages[j].staff == true) {
            var message = "<p><b>" + listOfMessages[j].message + "</b></p>";
          } else {
            var message = "<p>" + listOfMessages[j].message + "</p>";
          }
          let date = "<span>" + new Date(listOfMessages[j].date).toLocaleString() + "</span>";
          let messageContainer = '<div class="messageContainer">' + username + message + date + "</div>";
          messageList = messageList + messageContainer;
        }
      }
      if (document.getElementById("display").innerHTML == messageList) {
        request.abort();
      } else {
        document.getElementById("display").innerHTML = messageList;
        var interval = setInterval(scrollChatToBottom, 1000);
        setTimeout(function () {
          clearInterval(interval);
        }, 1000);
      }
    };
    request.send();
  }, 1000);
});

function scrollChatToBottom() {
  var display = document.getElementById("display");
  display.scrollTop = display.scrollHeight;
}

document.addEventListener("DOMContentLoaded", () => {
  const formPost = document.getElementById("post-form");
  formPost.addEventListener("submit", function (event) {
    event.preventDefault();
    let request = new XMLHttpRequest();
    request.open("POST", "/send/", true);
    const csrftoken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;
    request.setRequestHeader("X-CSRFToken", csrftoken);
    var room_id = document.getElementById("room_name").value;
    var message = document.getElementById("message").value;
    console.log(message)
    if (document.getElementById("message").value == "") {
      request.abort();
    } else {
      var message = document.getElementById("message").value;
    }
    var data = JSON.stringify({
      room_id: room_id,
      message: message,
    });
    request.send(data);
    document.getElementById("message").value = "";
  });
});
