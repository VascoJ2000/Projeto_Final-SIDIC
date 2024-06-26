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
    }).then(data => addFolderToFolder(data))
    .catch(err => console.log(err))
}

function deleteFolder(folder){
    fetch(url + `/folder/${folder}`, {
        method: 'DELETE',
    }).then(res => {
        if(res.status === 204) {
            return res.text()
        }
    }).then(data => getFolder(currentFolder))
    .catch(err => console.log(err))
}

function loadFolder(payload){
    currentWorkspace = payload.workspace_id
    currentFolder = payload.folder_id
    if(payload.is_root){
        worktable.innerHTML = `<thead>
                                   <tr>
                                       <th><div>
                                            ${payload.folder_name} 
                                            <button onclick="bsModalFolder.show()">New Folder</button>
                                            <button onclick="bsModalFiles.show()">Add Document</button>
                                       </div></th>
                                       <th></th>
                                       <th></th>
                                       <th></th>
                                   </tr>
                               </thead>`
    }else{
        worktable.innerHTML = `<thead>
                                   <tr>
                                       <th><div>
                                            <button onclick="getFolder('${payload.root_folder}')">^</button> 
                                            ${payload.folder_name} 
                                            <button onclick="bsModalFolder.show()">New Folder</button>
                                            <button onclick="bsModalFiles.show()">Add Document</button>
                                       </div></th>
                                       <th></th>
                                       <th></th>
                                       <th></th>
                                   </tr>
                               </thead>`
    }

    for(let i = 0; i<payload.folders.length; i++){
        const tbody = document.createElement('tbody')
        tbody.innerHTML = `
                            <tr>
                                <td onclick="getFolder('${payload.folders[i].folder_id}')">&#128193; ${payload.folders[i].name}</td>
                                <td></td>
                                <td><button onclick="deleteFolder('${payload.folders[i].folder_id}')">DELETE</button></td>
                                <td></td>
                            </tr>
        `
        worktable.appendChild(tbody)
    }
    for(let i = 0; i<payload.files.length; i++){
        const tbody = document.createElement('tbody')
        if(payload.files[i].name.slice(-4) === ".pdf"){
            tbody.innerHTML = `
                            <tr>
                                <td>${payload.files[i].name}</td>
                                <td><button onclick="getFile('${payload.files[i].file_id}')">GET</button></td>
                                <td><button onclick="deleteFile('${payload.files[i].file_id}')">DELETE</button></td>
                                <td><button onclick="resumePDF('${payload.files[i].file_id}')">RESUME</button></td>
                            </tr>
            `
        }else {
            tbody.innerHTML = `
                            <tr>
                                <td>${payload.files[i].name}</td>
                                <td><button onclick="getFile('${payload.files[i].file_id}')">GET</button></td>
                                <td><button onclick="deleteFile('${payload.files[i].file_id}')">DELETE</button></td>
                                <td></td>
                            </tr>
            `
        }
        worktable.appendChild(tbody)
    }
}

function addFolderToFolder(folder){
    const tbody = document.createElement('tbody')
    tbody.innerHTML = `
                        <tr>
                            <td onclick="getFolder('${folder.folder_id}')">&#128193; ${folder.name}</td>
                            <td></td>
                            <td><button onclick="deleteFolder('${payload.folders[i].folder_id}')">DELETE</button></td>
                        </tr>
    `
    worktable.appendChild(tbody)
}