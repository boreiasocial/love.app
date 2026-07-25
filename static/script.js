let imagens = [];
let indice = 0;
let tempo = 10000;

// =====================
// Carregar tempo
// =====================

fetch("/tempo")
.then(r => r.json())
.then(d => {

    tempo = d.segundos * 1000;

    carregarImagens();

});

// =====================
// Carregar imagens
// =====================

function carregarImagens(){

    fetch("/images")

    .then(r=>r.json())

    .then(lista=>{

        imagens = lista;

        if(imagens.length==0){

            return;

        }

        document
        .getElementById("slideshow")
        .src = imagens[0].url;

        setInterval(trocarImagem,tempo);

    });

}

function trocarImagem(){

    if(imagens.length<=1){

        return;

    }

    indice++;

    if(indice>=imagens.length){

        indice=0;

    }

    document
    .getElementById("slideshow")
    .src = imagens[indice].url;

}

// =====================
// Cartas
// =====================

function carregarCartas(){

    fetch("/letters")

    .then(r=>r.json())

    .then(lista=>{

        let div = document.getElementById("letters");

        div.innerHTML="";

        lista.forEach(carta=>{

            let item=document.createElement("div");

            item.className="carta";

            item.innerHTML=
            `
            💌
            <div class="tooltip">

            ${carta.title}

            <br>

            ${carta.date}

            </div>
            `;

            item.onclick=()=>abrirCarta(carta.id);

            div.appendChild(item);

        });

    });

}

carregarCartas();

// =====================
// Abrir carta
// =====================

function abrirCarta(id){

    fetch("/letter/"+id)

    .then(r=>r.json())

    .then(c=>{

        alert(

        c.title +

        "\n\n"

        + c.content +

        "\n\n"

        + c.author +

        "\n"

        + c.date

        );

    });

}
