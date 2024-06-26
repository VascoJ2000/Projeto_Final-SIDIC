const modalFiles = document.getElementById("modalFile");
const bsModalFiles = new bootstrap.Modal(modalFiles, (backdrop = "static")); // Pode passar opções

const fileInput = document.getElementById('fileInput')

function getFile(file){
    fetch(url + `/file/${file}`, {
        method: 'GET',
    }).then(res => {
        if(res.ok) {
            return res.json()
        }
    }).then(data => downloadFile(data))
    .catch(err => console.log(err))
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

function deleteFile(){

}

function resumePDF(){

}

function downloadFile(){

}

function addFileToFolder(file){
    const tbody = document.createElement('tbody')
    tbody.innerHTML = `
                        <tr>
                            <td>${file.name}</td>
                            <td><button onclick="getFile('${file.file_id}')">GET</button></td>
                            <td><button onclick="deleteFile('${file.file_id}')">DELETE</button></td>
                        </tr>
    `
    worktable.appendChild(tbody)
}