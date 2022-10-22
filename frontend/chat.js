// Croquet Tutorial 3
// Multiuser Chat
// Croquet Studios, 2019-2021

let previousPoster = ""
let chatSection = document.getElementById("chatSection")

class ChatModel extends Croquet.Model {
  
    init() {
      this.views = new Map();
      this.participants = 0;
      this.history = []; // { viewId, html } items
      this.lastPostTime = null;
      this.inactivity_timeout_ms = 60 * 1000 * 20; // constant
      this.subscribe(this.sessionId, "view-join", this.viewJoin);
      this.subscribe(this.sessionId, "view-exit", this.viewExit);
      this.subscribe("input", "newPost", this.newPost);
      this.subscribe("input", "reset", this.resetHistory);
    }
  
    viewJoin(viewId) {
      const existing = this.views.get(viewId);
      if (!existing) {
        const nickname = this.randomName();
        // const displayPic = this.randomDP();
        this.views.set(viewId, nickname);
      }
      this.participants++;
      this.publish("viewInfo", "refresh");  
    }
    
    viewExit(viewId) {
      this.participants--;
      this.views.delete(viewId);
      this.publish("viewInfo", "refresh");
    }
  
    newPost(post) {
      const postingView = post.viewId;
      const nickname = this.views.get(postingView)
      // console.log(previousPoster)
      // console.log(nickname)
      let chatLine = ""
      if (nickname == previousPoster) {
        chatLine = `
        <div class="flex gap-4 min-w-[250px] max-w-[33%] -mt-3 mb-5 my-text">
            <div class="flex flex-col gap-1 w-full">
                <div class="w-full bg-brand-purple text-white pl-5 text-base pr-7 py-[11px] font-montserrat font-medium rounded-lg rounded-tr-none break-all">
                  ${this.escape(post.text)}
                </div>
            </div>
        </div>
        `;
      } else {
        chatLine = `
        <div class="flex gap-4 min-w-[250px] max-w-[33%] my-5 my-text">
              <div class="flex flex-col gap-1 w-full">
                  <div class="flex justify-between font-quicksand font-semibold w-full h-fit">
                      <p class="text-gray-700 font-bold">You</p>
                      <p class="text-sm text-gray-600">11:40AM 10 Oct, 2022</p>
                  </div>
                  <div class="w-full bg-brand-purple text-white pl-5 text-base pr-7 py-[11px] font-montserrat font-medium rounded-lg rounded-tr-none break-all">
                    ${this.escape(post.text)}
                  </div>
              </div>
          </div>
        `;
      }
      this.addToHistory({ viewId: postingView, html: chatLine });
      this.lastPostTime = this.now();
      this.future(this.inactivity_timeout_ms).resetIfInactive();
      previousPoster = nickname
    }
  
    addToHistory(item){
      this.history.push(item);
      if (this.history.length > 100) this.history.shift();
      this.publish("history", "refresh");   
    }
  
    resetIfInactive() {
      if (this.lastPostTime !== this.now() - this.inactivity_timeout_ms) return;
      
      this.resetHistory("due to inactivity");
    }
    
    resetHistory(reason) {
      this.history = [{ html: `<span class="mb-3 font-medium font-alternates text-[15px] block">Chat Reset ${reason}</span>` }];
      this.lastPostTime = null;
      this.publish("history", "refresh");
    }
    
    escape(text) { // Clean up text to remove html formatting characters
      return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
    }
  
    randomName() {
      // const names =["Acorn", "Allspice", "Almond", "Ancho", "Anise", "Aoli", "Apple", "Apricot", "Arrowroot", "Asparagus", "Avocado", "Baklava", "Balsamic", "Banana", "Barbecue", "Bacon", "Basil", "Bay Leaf", "Bergamot", "Blackberry", "Blueberry", "Broccoli", "Buttermilk", "Cabbage", "Camphor", "Canaloupe", "Cappuccino", "Caramel", "Caraway", "Cardamom", "Catnip", "Cauliflower", "Cayenne", "Celery", "Cherry", "Chervil", "Chives", "Chipotle", "Chocolate", "Coconut", "Cookie Dough", "Chamomile", "Chicory", "Chutney", "Cilantro", "Cinnamon", "Clove", "Coriander", "Cranberry", "Croissant", "Cucumber", "Cupcake", "Cumin", "Curry", "Dandelion", "Dill", "Durian", "Earl Grey", "Eclair", "Eggplant", "Espresso", "Felafel", "Fennel", "Fig", "Garlic", "Gelato", "Gumbo", "Halvah", "Honeydew", "Hummus", "Hyssop", "Ghost Pepper", "Ginger", "Ginseng", "Grapefruit", "Habanero", "Harissa", "Hazelnut", "Horseradish", "Jalepeno", "Juniper", "Ketchup", "Key Lime", "Kiwi", "Kohlrabi", "Kumquat", "Latte", "Lavender", "Lemon Grass", "Lemon Zest", "Licorice", "Macaron", "Mango", "Maple Syrup", "Marjoram", "Marshmallow", "Matcha", "Mayonnaise", "Mint", "Mulberry", "Mustard", "Natto", "Nectarine", "Nutmeg", "Oatmeal", "Olive Oil", "Orange Peel", "Oregano", "Papaya", "Paprika", "Parsley", "Parsnip", "Peach", "Peanut Butter", "Pecan", "Pennyroyal", "Peppercorn", "Persimmon", "Pineapple", "Pistachio", "Plum", "Pomegranate", "Poppy Seed", "Pumpkin", "Quince", "Raspberry", "Ratatouille", "Rosemary", "Rosewater", "Saffron", "Sage", "Sassafras", "Sea Salt", "Sesame Seed", "Shiitake", "Sorrel", "Soy Sauce", "Spearmint", "Strawberry", "Strudel", "Sunflower Seed", "Sriracha", "Tabasco", "Tahini", "Tamarind", "Tandoori", "Tangerine", "Tarragon", "Thyme", "Tofu", "Truffle", "Tumeric", "Valerian", "Vanilla", "Vinegar", "Wasabi", "Walnut", "Watercress", "Watermelon", "Wheatgrass", "Yarrow", "Yuzu", "Zucchini"];
      const names = ["Giver", "Follower"]
      return names[Math.floor(Math.random() * names.length)];
    }

    randomDP() {
      const profilePics = ["profile-1.jpg", "profile-2.jpg", "profile-3.jpg", "profile-4.jpg", "profile-5.jpg", "profile-6.jpg", "profile-7.jpg", "profile-8.jpg"]
      return profilePics[Math.floor(Math.random() * profilePics.length)];
    }
  }
  
  ChatModel.register("ChatModel");
  
  class ChatView extends Croquet.View {
  
    constructor(model) {
      super(model);
      this.model = model;
      sendButton.onclick = () => this.send();
      this.subscribe("history", "refresh", this.refreshHistory);
      this.subscribe("viewInfo", "refresh", this.refreshViewInfo);
      this.refreshHistory();
      this.refreshViewInfo();
      if (model.participants === 1 &&
        !model.history.find(item => item.viewId === this.viewId)) {
        this.publish("input", "reset", "for new participants");
      }
    }
  
    send() {
      const text = textIn.value;
      textIn.value = "";
      if (text === "/reset") {
        this.publish("input", "reset", "at user request");
      } else {
        this.publish("input", "newPost", {viewId: this.viewId, text});    
        window.setTimeout(() => {
          chatSection.scrollTo({
            "top": document.body.scrollHeight,
            "behavior": "smooth",
          })
        }, 280)
      }
    }
   
    refreshViewInfo() {
      nickname.innerHTML = `${this.model.views.get(this.viewId)}`;
      document.getElementById("display-picture").setAttribute("src", "images/" + this.model.randomDP());
      viewCount.innerHTML = `<span class="font-semibold mr-2">Participants:</span> ` + this.model.participants;
    }
  
    refreshHistory() {
      textOut.innerHTML = `<p class="font-bold font-quicksand">Welcome to the Chat!</p>` + 
        this.model.history.map(item => item.html).join("");
      textOut.scrollTop = Math.max(10000, textOut.scrollHeight);
    }
  }
  
  Croquet.Session.join({
    appId: "io.codepen.croquet.chat",
    apiKey: "1_9oolgb5b5wc5kju39lx8brrrhm82log9xvdn34uq",
    name: "unnamed",
    password: "secret",
    model: ChatModel,
    view: ChatView
  });
