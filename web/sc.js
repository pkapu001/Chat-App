let msgbox;
var username = "";
var friend = "";

function setuser(ret) {
  username = ret[0];
  friend = ret[1];
  var ele = document.getElementById("title");
  ele.innerHTML = friend;
}

window.onload = function() {
  var textbox = document.getElementById("textbox");
  textbox.addEventListener("keydown", function(e) {
    if (e.keyCode === 13) {
      //checks whether the pressed key is "Enter"
      btnclick();
    }
  });

  eel.setdata()(setuser);
  console.log("pageloading");
  msgbox = document.getElementById("msgbox");
  msgbox.addEventListener("DOMSubtreeModified", scroll);
};

function scroll() {
  msgbox.scrollTop = msgbox.scrollHeight;
}

function sendmsg() {
  var textbox = document.getElementById("textbox");
  var data = textbox.value;
  textbox.value = "";
  if (data != "") {
    temp = document.getElementById("template-self");
    var cln = temp.content.cloneNode(true);
    var h4 = cln.querySelector("h4");
    var msg = cln.querySelector("label");
    var msgbox = document.getElementById("msgbox");
    eel.sendmsg(data);
    h4.innerHTML = username;
    msg.innerHTML = data;
    msgbox.append(cln);
  }
}

eel.expose(receivemsg);
function receivemsg(msg) {
  var data = msg;
  temp = document.getElementById("template-other");
  var cln = temp.content.cloneNode(true);
  var h4 = cln.querySelector("h4");
  var msg = cln.querySelector("label");
  var msgbox = document.getElementById("msgbox");
  h4.innerHTML = friend;
  msg.innerHTML = data;
  msgbox.append(cln);
}

// function startchat() {
//   var un = document.getElementById("username").value;
//   var other = document.getElementById("msgto").value;
//   document.location.href = "chat.html";
// }

// eel.expose(say_hello_js); // Expose this function to Python
// function say_hello_js(x) {
//   console.log("Hello from " + x);
// }
