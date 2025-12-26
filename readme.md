<style> 
    body {
        background: #111;
        padding-top: 4.5rem;
    }
    details{
        margin-left: auto;
        padding: 0.2rem 0.8rem;
        width: fit-content;
    }
    marquee {
        /* background:#1a1a1a;  */
        color: #f01b1bff; 
        font-weight: 600;
        font-size: 1.3rem;
        /* margin: -1.5rem -3.5rem 0; */
        box-shadow: -10px 0 0 0 red;
        position: absolute;
        inset: 0 0 auto 0;
        padding: 1rem 0;
        z-index: 2;
    }
    h1 {
        margin-top: -2rem;
        pointer-events: none;
    }
</style>
<details> 
<summary>TOGGLE NEWS</summary> 


<marquee behavior="scroll" scrollamount="14">
BREAKING: Experts shocked as issue resolves itself overnight. 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
JUST IN: Situation unchanged, but now with more urgency.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
DEVELOPING: Experts split between optimism and concern.
</marquee>
</details>

# The News
A database with articles from over the whole world.
> **[https://news-q92k.onrender.com/](https://news-q92k.onrender.com/)**

## Features
<input type="checkbox" checked> auto-fetch headlines hourly <br>
<input type="checkbox" checked> search articles <br> 
<input type="checkbox" checked> save articles <br>
<input type="checkbox"> create user account <br>
<input type="checkbox"> delete articles <br>

## To Do
- add Github workflow logs
    - how many articles fetched?
    - what action (isUpdated, isNewSave or isIncomplete)?
    - fetched when?
- add page to monitor workflow logs
- add link to admin
- update article model to show if headline or a user-saved article
- auto-fetch headlines from other countries
- add button to delete article
- add dark/light mode
- add news attributes
    - location
    - category
- allow filtering and sorting of headlines and my_articles
- allow user to set headlines fetch preferences 
    - sources
    - location
- get better services 
    - URL
    - Render takes minutes to wake up
    - Render does not have CLI
    - Github actions are inconsistent
