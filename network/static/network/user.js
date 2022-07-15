document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('follow').onclick = () => {
        fetch(`/user/${document.getElementById('follow').dataset.userr}`, {
            method:"POST"
        })
        .then(response => response.json())
        .then(msg => {
            if(msg.followstatus == "following"){
                document.getElementById('follow').innerHTML = "Unfollow";
                document.getElementById('followers').innerHTML = parseInt(document.getElementById('followers').innerHTML) + 1;
            } else {
                document.getElementById('follow').innerHTML = "Follow";
                document.getElementById('followers').innerHTML = parseInt(document.getElementById('followers').innerHTML) - 1;
            }
        });
    }
});