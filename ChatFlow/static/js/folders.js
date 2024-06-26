const modalFolder = document.getElementById("modalFolder");
const bsModalFolder = new bootstrap.Modal(modalFolder, (backdrop = "static")); // Pode passar opções

const folderInfo = document.getElementById('folderInfo')

let currentFolder = null

function getFolder(folder){
    showWorkspace(false)
    fetch(url + `/folder/${folder}`, {
        method: 'GET',
    }).then(res => {
        if(res.ok) {
            return res.json()
        }
    }).then(data => loadFolder(data))
    .catch(err => console.log(err))
}

function addFolder(){
    const folder_name = document.getElementById('folderName').value
    fetch(url + `/folder`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            folder_name: folder_name,
            root_folder: currentFolder,
            workspace_id: currentWorkspace
        }),
    }).then(res => {
        if(res.ok) {
            return res.json()
        }
    }).then(data => loadFolder(data))
    .catch(err => console.log(err))
}

function loadFolder(payload){
    currentWorkspace = payload.workspace_id
    currentFolder = payload.folder_id
    if(payload.is_root){
        worktable.innerHTML = `<thead>
                                   <tr>
                                       <th><div>${payload.folder_name} <button onclick="bsModalFolder.show()">New Folder</button></div></th>
                                       <th></th>
                                       <th></th>
                                   </tr>
                               </thead>`
    }else{
        worktable.innerHTML = `<thead>
                                   <tr>
                                       <th><div><button onclick="getFolder('${payload.root_folder}')">^</button> ${payload.folder_name} <button onclick="bsModalFolder.show()">New Folder</button></div></th>
                                       <th></th>
                                       <th></th>
                                   </tr>
                               </thead>`
    }
    const tbody = document.createElement('tbody')
    console.log(payload.folders)
    for(let i = 0; i<payload.folders.length; i++){
        tbody.innerHTML = `
                            <tr>
                                <td onclick="getFolder('${payload.folders[i].folder_id}')">&#128193; ${payload.folders[i].name}</td>
                                <td></td>
                                <td></td>
                            </tr>
        `
    }
    for(let i = 0; i<payload.files.length; i++){
        tbody.innerHTML = `
                            <tr>
                                <td>${payload.files[i].name}</td>
                                <td><button onclick="getFile('${payload.file[i].folder_id}')">GET</button></td>
                                <td><button onclick="deleteFile('${payload.file[i].folder_id}')">DELETE</button></td>
                            </tr>
        `
    }
    worktable.appendChild(tbody)
}