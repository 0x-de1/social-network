document.addEventListener('DOMContentLoaded', function () {
  console.log('Page loaded');

  let followingButton = document.querySelector('#following-btn');
  if (followingButton) {
    followingButton.onmouseenter = () => {
      console.log(followingButton);
      followingButton.querySelector('span').innerText = 'Unfollow';
      followingButton.classList.remove('btn-success');
      followingButton.classList.add('btn-danger');
    };
    followingButton.onmouseleave = () => {
      console.log(followingButton);
      followingButton.querySelector('span').innerText = 'Following';
      followingButton.classList.remove('btn-danger');
      followingButton.classList.add('btn-success');
    };
  }
  let editButtons = document.querySelectorAll('#edit-post-button');
  if (editButtons) {
    editButtons.forEach((button) => {
      button.onclick = () => {
        let post = button.parentNode.parentNode.parentNode;
        let postContent = post.querySelector('#post-content').innerText;
        // console.log(post);
        let editPost = post.parentNode.querySelector('#edit-post');
        console.log(editPost);
        let textArea = post.parentNode.querySelector('#edit-post-form');
        post.style.display = 'none';
        editPost.style.display = 'flex';
        textArea.value = postContent;
        console.log(editPost.querySelector('#post-button'));
        editPost.querySelector('#post-button').onclick = () => {
          submit_edited_post(button.dataset.postId, textArea.value);
          post.style.display = 'flex';
          editPost.style.display = 'none';
          post.querySelector('#post-content').innerText = textArea.value;
          console.log(button.dataset.postId, textArea.value);
        };
      };
    });
  }
  let likeButtons = document.querySelectorAll('#like-btn');
  console.log(likeButtons);

  if (likeButtons) {
    var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    console.log(csrf_token);
    likeButtons.forEach((button) => {
      button.onclick = () => {
        fetch(`/likes/${button.dataset.postId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
          },
        })
          .then((response) => response.json())
          .then((data) => {
            // If email was sent
            console.log('got data', data);
            if (data !== undefined) {
              console.log(data.message);
              button.parentElement.querySelector('#like-count').innerText =
                likes(data.likes);
              if (data.likes !== 0) {
                button.classList.remove('btn-outline-secondary');
                button.classList.add('btn-outline-danger');
              } else {
                button.classList.remove('btn-outline-danger');
                button.classList.add('btn-outline-secondary');
              }
            } else if (data.error !== undefined) {
              console.error('got error', data);
            }
          })
          .catch((error) => {
            console.error('Errorr:', error);
          });
      };
    });
  }
});

function likes(like_count) {
  if (like_count > 1) {
    return `${like_count} Likes`;
  } else if (like_count === 1) {
    return `${like_count} Like`;
  } else {
    return 'Like';
  }
}
// async function sumbit_edited_post(post_id, new_content) {
//   post_data = {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//       'X-CSRFToken': csrf_token,
//     },
//     body: JSON.stringify({
//       content: new_content,
//     }),
//   };
//   console.log(post_data);
//   try {
//     const response = await fetch(`/edit_post/${post_id}`, post_data);
//     console.log(response);

//     const data = await response.json();
//     if (!data.ok) {
//       console.error(response);
//       throw new Error(`HTTP error! status: ${response}`);
//     }
//     console.log(data);
//   } catch (error) {
//     console.error('Error:', error);
//   }
// }

function submit_edited_post(post_id, new_content) {
  var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  console.log(
    'Submitting edited post with ID',
    post_id,
    'and new content',
    new_content
  );

  fetch(`/edit_post/${post_id}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token, // use your CSRF token here
    },
    body: JSON.stringify({
      content: new_content,
    }),
  })
    .then((response) => {
      console.log('Received response with status', response.status);
      if (!response.ok) {
        throw new Error(response.status);
      }
      return response.json();
    })
    .then((data) => {
      console.log('Received data:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// function sumbit_edited_post(post_id, new_content) {
//   fetch(`/edit_post/${post_id}`, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//       'X-CSRFToken': csrf_token,
//     },
//     body: JSON.stringify({
//       content: new_content,
//     }),
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       // If email was sent
//       console.log('got data', data);
//       if (data !== undefined) {
//         console.log(data.message);
//       } else if (data.error !== undefined) {
//         console.error('got error', data);
//       }
//     })
//     .catch((error) => {
//       console.error('Errorr:', error);
//     });
// }
