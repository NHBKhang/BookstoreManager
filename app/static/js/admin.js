function deleteBook(bookId) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch(`/admin/delete_book/${bookId}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            let c = document.getElementById(`book${bookId}`)
            c.style.display = "none"
        }).catch(err => console.info(err)) // promise
    }
}
