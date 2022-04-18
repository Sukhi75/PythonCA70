function deleteScribble(noteId) {
  fetch("/delete-inscription", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
