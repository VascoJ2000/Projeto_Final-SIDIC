const chatInput = document.getElementById('message')
const chatHistory = document.getElementById('chat-history')
const loading = document.getElementById('loading')
let currentChat = null

const asideChat = document.getElementById('asideChat')


function selectChat(chatName) {
    currentChat = chatName
    chatHistory.innerHTML = ''
}

function getChats(){
    fetch(url + `/chats`, {
        method: 'GET',
    }).then(res => {
        if(res.ok) {
            return res.json()
        }
    }).then(data => loadChats(data))
    .catch(err => console.log(err))
}

function getChatMessages(chat_id) {
    selectChat(chat_id)
    loading.innerHTML = 'Loading chat...'
    loading.style.display = 'block'
    fetch(url + `/chat/${chat_id}`, {
        method: 'GET',
    }).then(res => {
        if(res.ok) {
            loading.style.display = 'none'
            return res.json()
        }
    }).then(data => loadChatMessages(data))
    .catch(err => {
        console.log(err)
        loading.innerHTML = 'Could not load messages!'
    })
}

function sendMessage() {
    const mes = chatInput.value.trim()
    fetch(url + `/chats`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: mes,
            chat_id: currentChat == null ? false : currentChat
        }),
    }).then(res => {
        if(res.ok) {
            return res.json()
        }
    }).then(data => {
        if(currentChat == null){
            getChats()
            selectChat(data.chat_id)
        }
        addToChat({role: 'user', content: mes})
        return mesReceived(data)
    }).catch(err => console.log(err))
}

function loadChats(payload){
    asideChat.innerHTML = ''
    console.log(payload)
    for(let i = 0; i<payload.length; i++){
        asideChat.innerHTML += `<li><a href="#" class="d-inline-flex text-white rounded" onclick="getChatMessages('${payload[i].chat_id}')">${payload[i].name}</a></li>`
    }
}

function loadChatMessages(mes){
    for (let i = 0; i<mes.length; i++) {
        console.log(mes[i])
        addToChat(mes[i].message)
    }
}

function mesReceived(payload){
    addToChat(payload.message)
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