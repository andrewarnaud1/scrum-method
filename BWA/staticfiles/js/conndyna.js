const sinscrire = document.getElementById('sinscrire');

sinscrire.style.display = 'none';

//créer la fonction cacheurform()
function cacheurform(idform) {
    if (idform == 'sinscrire') {
        document.getElementById('seconnecter').style.display = 'block';
        document.getElementById('sinscrire').style.display = 'none';
    } else {
        document.getElementById('seconnecter').style.display = 'none';
        document.getElementById('sinscrire').style.display = 'block';
    }
}
