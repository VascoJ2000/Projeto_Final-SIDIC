const modalFiles = document.getElementById("modalFile");
const bsModalFiles = new bootstrap.Modal(modalFiles, (backdrop = "static")); // Pode passar opções

const fileInput = document.getElementById('fileInput')

function getFile(file){
    window.location.href = `/file/${file}`;
}

function uploadFile(){
    const file = fileInput.files[0]
    const formData = new FormData()
    formData.append('file', file)
    fetch(url + `/file/${currentFolder}`, {
        method: 'POST',
        body: formData
    }).then(res => {
        if(res.ok) {
            return res.json()
        }
    }).then(data => addFileToFolder(data))
    .catch(err => console.log(err))
}

function deleteFile(file){
    fetch(url + `/file/${file}`, {
        method: 'DELETE',
    }).then(res => {
        if(res.status === 204) {
            return res.text()
        }
    }).then(data => getFolder(currentFolder))
    .catch(err => console.log(err))
}

function resumePDF(file){
    fetch(url + `/file/resume/${file}`, {
        method: 'GET',
    }).then(res => {
        if(res.ok) {
            return res.json()
        }
    }).then(data => loadChat(data))
    .catch(err => console.log(err))
}

function addFileToFolder(file){
    const tbody = document.createElement('tbody')
    if(file.name.slice(-4) === ".pdf") {
        tbody.innerHTML = `
                        <tr>
                            <td>${file.name}</td>
                            <td><button onclick="getFile('${file.file_id}')">GET</button></td>
                            <td><button onclick="deleteFile('${file.file_id}')">DELETE</button></td>
                            <td><button onclick="resumePDF('${file.file_id}')">RESUME</button></td>
                        </tr>
        `
    }else{
        tbody.innerHTML = `
                        <tr>
                            <td>${file.name}</td>
                            <td><button onclick="getFile('${file.file_id}')">GET</button></td>
                            <td><button onclick="deleteFile('${file.file_id}')">DELETE</button></td>
                            <td></td>
                        </tr>
        `
    }
    worktable.appendChild(tbody)
}