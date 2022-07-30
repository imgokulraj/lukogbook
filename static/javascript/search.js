async function getProfile(){
    const searchText = document.querySelector('#searchprofile').value       
    let res = await fetch(`/profile/search/${searchText}`,{
        method : "GET" ,
        headers : {
            'Content-Type' : 'application/json'
        }
    })
    res = await res.json()
    document.querySelector('.output').innerHTML = ''
    res.forEach( (val) => {
        const div = document.createElement('div') 
        div.classList.add('profile-container')
        div.innerHTML = `<div class="searchlinks"><p>Username : ${val[0]}</p>
        <a href="/profile/others/${val[0]}">Go to profile</a>
        <p>To chat <a href="/profile/search/adduser/${val[0]}">Click here</a></p>
        </div>
        <img src="${'/' + val[1]}" alt="">
        `
        document.querySelector('.output').appendChild(div) 
    })
}

document.querySelector('#searchprofile').addEventListener('keyup' , (e) => {
    getProfile()
})