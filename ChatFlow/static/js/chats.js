const chatInput = null
const chatHistory = null
let currentChat = null


function selectChat(chatName) {
    currentChat = chatName
}

async function getChats(){
    await fetch(url + `/chats`, {
        method: 'GET',
    }).then(res => {
        if(res.ok) {
            console.log(res.text())
            loadChats(res.json())
        }
    }).catch(err => console.log(err))
}

async function getChatMessages(chat_id) {
    currentChat = chat_id
    await fetch(url + `/chat/${chat_id}`, {
        method: 'GET',
    }).then(res => {
        if(res.ok) {
            console.log(res.text())
            loadChatMessages(res.json())
        }
    }).catch(err => console.log(err))
}

async function sendMessage() {
    await fetch(url + `/chats`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: chatInput.value.trim(),
            chat_id: false
        }),
    }).then(res => {
        if(res.ok) {
            console.log(res.text())
            mesReceived(res.json())
        }
    }).catch(err => console.log(err))
}

function loadChats(payload){

}

function loadChatMessages(chat){
    const mes = chat.messages
    for (let i = 0; i<mes.length; i++) {
        console.log(mes[i])
        addToChat(mes[i])
    }
}

function mesReceived(payload){
    const mes = JSON.parse(payload.body)
    addToChat(mes)
}

function addToChat(mes){
    if (mes.role == 'user'){
        chatHistory.innerHTML += `<div class="message outgoing">
                                    <div>${mes.content}</div>
                                  </div>`
    }else{
        chatHistory.innerHTML += `<div class="message incoming">
                                    <div>${mes.content}</div>
                                  </div>`
    }
    chatHistory.scrollTop = chatHistory.scrollHeight - chatHistory.clientHeight;
}