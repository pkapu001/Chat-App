// function startchat() {
//   var un = document.getElementById("username").value;
//   var other = document.getElementById("msgto").value;
//   document.location.href = "chat.html";
//   eel.getdata(un, other);

//   console.log(`${un}     |  ${other}`);
// }

async function signup() {
  var un = document.getElementById("username");
  var p1 = document.getElementById("password1");
  var p2 = document.getElementById("password2");
  console.log("signup clicked", p1.value, p2.value);
  var conform = false;
  if (p1.value == p2.value) {
    conform = await eel.signup(un.value, p1.value)();
  } else {
    p1.value = "";
    p2.value = "";
    p1.placeholder = "passwords didnt match";
    p2.placeholder = "passwords didnt match";
  }
  if (conform) {
    document.location.href = "friendname.html";
  } else {
    un.value = "";
    un.placeholder = "username already in USE";
    p1.value = "";
    p2.value = "";
  }
}

async function login() {
  var un = document.getElementById("username");
  var pas = document.getElementById("password");
  var conform = await eel.login(un.value, pas.value)();
  console.log(conform);
  if (conform) {
    document.location.href = "friendname.html";
  } else {
    un.value = "";
    pas.value = "";
    un.placeholder = "incorrect username or password";
    pas.placeholder = "incorrect username or password";
  }
}

async function startchat() {
  var friend = document.getElementById("friendname");
  var conform = await eel.startchat(friend.value)();
  if (conform) {
    document.location.href = "chat.html";
    // eel.getdata(friend.value);
  } else {
    friend.value = "";
    friend.placeholder = "friend not found";
  }
}

// eel.expose(say_hello_js); // Expose this function to Python
// function say_hello_js(x) {
//   console.log("Hello from " + x);
// }
// say_hello_js("satring");
