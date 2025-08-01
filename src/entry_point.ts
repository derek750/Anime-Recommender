import { Anime } from "./datatypes.js";

const url : string = "http://127.0.0.1:5000/api";

function testData() : void{
    const dataurl : string = `${url}/dataset`;
    fetch(dataurl)
        .then(res => res.json())
        .then((data: Anime[]) => {
        console.log(data);  
        console.log(data.length);
    });
}

testData();
