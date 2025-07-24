import { Anime } from "./datatypes.js";

const url : string = "http://127.0.0.1";

function testData() : void{
    const dataurl : string = `${url}/dataset`;
    fetch(dataurl)

        .then(res => res.json())

        .then((data: Anime[]) => {
        console.log(data);      
        console.log(data[0].title) 
    });
    console.log("A")
}

testData();
