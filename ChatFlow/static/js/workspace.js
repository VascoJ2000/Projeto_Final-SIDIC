const modalWorkspace = document.getElementById("modalWorkspace");
const bsModalWorkspace = new bootstrap.Modal(modalWorkspace, (backdrop = "static")); // Pode passar opções
const btnWorkspace = document.getElementById('newSpace');

const drive = document.getElementById('drive')
const chatAI = document.getElementById('chat')

const asideWorkspace = document.getElementById('asideWorkspace')
const worktable = document.getElementById('Worktable')

let currentWorkspace = null

btnWorkspace.addEventListener('click', () => {
    bsModalWorkspace.show()
});

function showWorkspace(space){
    if (space){
        drive.style.display = 'none'
        chatAI.style.display = 'block'
    }else{
        drive.style.display = 'block'
        chatAI.style.display = 'none'
    }
}

function getWorkspaces(){
    fetch(url + `/workspace`, {
        method: 'GET',
    }).then(res => {
        if(res.ok) {
            return res.json()
        }
    }).then(data => loadWorkspaces(data))
    .catch(err => console.log(err))
}

function postWorkspace(){
    const name = document.getElementById('workspaceName').value
    fetch(url + `/workspace`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            workspace_name: name
        }),
    }).then(res => {
        if(res.ok) {
            showWorkspace(false)
            getWorkspaces()
            return res.statusText
        }
    }).then(data => console.log(data))
    .catch(err => console.log(err))
}

function deleteWorkspace(workspace){
    fetch(url + `/workspace/${workspace}`, {
        method: 'DELETE',
    }).then(res => {
        if(res.ok) {
            return res.json()
        }
    }).then(data => loadWorkspaces(data))
    .catch(err => console.log(err))
}

function putWorkspace(){
    const name = document.getElementById('workspaceName').value
    fetch(url + `/workspace`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            workspace_name: name
        }),
    }).then(res => {
        if(res.ok) {
            getWorkspaces()
            return res.statusText
        }
    }).then(data => console.log(data))
    .catch(err => console.log(err))
}

function loadWorkspaces(payload){
    const workspaces = payload.workspaces
    asideWorkspace.innerHTML = ''
    for(let i = 0; i<workspaces.length; i++){
        asideWorkspace.innerHTML += `<li><a href="#" class="d-inline-flex text-white rounded" onclick="getFolder('${workspaces[i].root_folder}')">${workspaces[i].workspace_name}</a></li>`
    }
}