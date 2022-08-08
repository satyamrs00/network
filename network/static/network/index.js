document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.newpost').style.display = document.querySelector('.newpost').dataset.display;

    var editbuttons = document.querySelectorAll('.edit')
    editbuttons.forEach(button => {
        button.onclick = () => {
            
            console.log(button.dataset.post_id);
            fetch(`/post/${button.dataset.post_id}`)
            .then(response => response.json())
            .then(post => {
                if(document.getElementById('editpost') === null){
                    var children = load_form(post);
                }
                var editpost = document.getElementById('editpost');
                console.log(editpost.dataset);
                editpost.onclick = () => {
                    fetch(`/post/${editpost.dataset.post_id}`, {
                        method: 'PUT',
                        body:JSON.stringify({
                            message: `${document.getElementById('txt').value}`,
                            is_edited: true
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log("here");

                        console.log(data);
                        load_post(data, children);
                    });
                }            
            });
        }

    });

    const likebuttons = document.querySelectorAll('.like');
    likebuttons.forEach(likebutton => {
        likebutton.onclick = () => {
            fetch(`/post/${likebutton.dataset.post_id}`, {
                method: "POST"
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                const likesshow = document.getElementById(`likes${likebutton.dataset.post_id}`)
                if(data.newlikescount > parseInt(likesshow.innerHTML)){
                    likebutton.classList.replace('fa-heart-o', 'fa-heart');
                } else {
                    likebutton.classList.replace('fa-heart', 'fa-heart-o');
                }
                likesshow.innerHTML = `${data.newlikescount}`;
            })
        }    
    })
});

function load_form(post){
    let label = document.createElement('label');
    let textarea = document.createElement('textarea');
    let button = document.createElement('button');
    label.setAttribute('for', 'txt');
    label.innerHTML = "Edit Post:";
    textarea.setAttribute('name', 'message');
    textarea.setAttribute('id', 'txt');
    textarea.innerHTML = post.message;
    button.innerHTML = "Post";
    button.setAttribute('id', 'editpost');
    button.setAttribute('data-post_id', `${post.id}`);
    
    var postdiv = document.getElementById(`post${post.id}`);
    const children = postdiv.children;
    const childrena = [];
    for(let i = 0; i < children.length;i++){
        childrena.push(children[i]);
    }
    while (postdiv.firstChild) {
        postdiv.removeChild(postdiv.lastChild);
    }
    postdiv.appendChild(label);
    postdiv.appendChild(textarea);
    postdiv.appendChild(button);

    return childrena;
}

function load_post(data, children) {
    postdiv = document.getElementById(`post${editpost.dataset.post_id}`);
    while(postdiv.firstChild){
        postdiv.removeChild(postdiv.lastChild);
    }
    postdiv.appendChild(children[0]);
    children[1].innerHTML = `${data.edited_message}`;
    postdiv.appendChild(children[1]);
    if(children.length === 5){
        let edited = document.createElement('div');
        edited.classList.add('dt');
        edited.innerHTML = "(edited)";
        console.log(postdiv);
        console.log(edited);
        postdiv.appendChild(edited);
    }
    for(let i = 2; i < children.length; i++){
        postdiv.appendChild(children[i]);
    }
}