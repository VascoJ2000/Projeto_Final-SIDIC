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

}

function deleteFile(){

}

function resumePDF(){

}

function downloadFile(){

}