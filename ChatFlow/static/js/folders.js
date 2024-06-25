const folderInfo = document.getElementById('folderInfo')

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

function loadFolder(payload){
    if(payload.is_root){
        folderInfo.innerHTML = `<div>${payload.folder_name}</div>`
    }else{
        folderInfo.innerHTML = `<div><button onclick="getFolder('${payload.root_folder}')">^</button> ${payload.folder_name}</div>`
    }
    const tbody = document.createElement('tbody')
    for(let i = 0; i<payload.folders.length; i++){
        tbody.innerHTML = `
                            <tr>
                                <td onclick="getFolder('${payload.folders[i].folder_id}')">${payload.folders[i].name}</td>
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