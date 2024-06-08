require('dotenv').config();
const prefix = "!";

// console.log(process.env.TOKEN);

const { Client, IntentsBitField } = require('discord.js');

const client = new Client({
    intents: [
        IntentsBitField.Flags.Guilds,
        IntentsBitField.Flags.GuildMembers,
        IntentsBitField.Flags.GuildMessages,
        IntentsBitField.Flags.MessageContent,
    ],
});

// client.on('ready', (c) =>{
//     console.log(`${c.user.tag} is online`);
// });
// client.on('messageCreate', (message) => {
//     console.log(message.content);
// }); // testing function for message create 
client.on('messageCreate', (message) => {
    // console.log(message.content);
    if(message.author.bot){
        // console.log(message.content);
        return;
    }
    if(message.content === 'piri no' || message.content === 'no piri' || message.content === 'NO piri' || message.content === 'nopiri'){
        message.reply(`NO YOU TOO ${message.author.globalName} <:fern_pout:1239754197952630814>`)
        // message.reply(`<:fern_pout:1239754197952630814>`)
    }
});
client.on('interactionCreate', interaction =>{
    if(!interaction.isChatInputCommand()) return;
    // console.log(interaction);
    if(interaction.commandName === 'sayhello'){
        const randInt = Math.floor(Math.random() * 3) + 1;
        if(interaction.user.id === '192697546446077953'){
            // interaction.reply("NO <@"+interaction.user.id+">")
            // interaction.reply({content : "NO <@"+interaction.user.id+">", fetchReply : true}).react('1239755005397958708');
            interaction.reply("NO <@"+interaction.user.id+"> <:fern_pout:1224356099461873714>")
        }
        else if(randInt === 1){
            interaction.reply("I don't want to say hello to <@"+interaction.user.id+">")
        }
        else{
            interaction.reply(`Hello I'm Sucrose, a researcher of alchemy, it's nice to meet you ${interaction.user.globalName}, I'd love to hear any stories you have about your adventures`)
        }
    }
})
client.on('interactionCreate', interaction =>{
    if(!interaction.isChatInputCommand()) return;
    // console.log(interaction);
    if(interaction.commandName === 'sayloveyou'){
        var result = interaction.options.get('person-name').value;
        // console.log(result);
        const randInt = Math.floor(Math.random() * 3) + 1;
        if(randInt===1){
            interaction.reply(`Love you ${result} 💖`);
        }
        else if(randInt === 2){
            interaction.reply(`Love you ${result} <:klee_hug:1068801227917381652>`);
        }
        else if(randInt=== 3){
            interaction.reply(`Love you ${result} <:clara_heart:1163509399579537439>`);
        }
    }
})
client.on('interactionCreate', (interaction) =>{
    if(!interaction.isChatInputCommand()) return;
    // console.log(interaction);
    if(interaction.commandName === 'aboutme'){
        const randInt = Math.floor(Math.random() * 3) + 1;
        switch(randInt) {
            case 1:
              interaction.reply("If you're busy, please don't let me stand in the way of progress. ...You're not busy? Really? It's fine, I—I get that you have stuff to do. I'm already quite used to working alone. ...You're truly not busy? I—In that case, I don't suppose you could help me with a few things? Or, you know, we could sit and chat about... stuff.");
              break;
            case 2:
              interaction.reply("Let me tell you a little secret, something I've never told anyone. The purpose behind my research is to create my own wonderland. Yes... just like the ones in fairy tales. The kind where all your dreams come true and you live happily ever after. Hehe, it's childish, isn't it? But, I still believe in fairy tales.")
              break;
            case 3:
              interaction.reply("Oh, you, ahh... noticed. My ears are a hereditary feature... quite different from everyone else's. So, I try to hide them with my hair as much as possible.")
              break;
            default:
                // console.log("This should not run tbh!!") 
          }
    }
})
client.on('interactionCreate', (interaction) => {
    if(!interaction.isChatInputCommand()) return;
    // console.log(interaction);
    if(interaction.commandName === 'artifact_value'){
        const atk = interaction.options.get('main-stat').value;
        let cr = interaction.options.get('crit-rate').value;
        let cd = interaction.options.get('crit-damage').value;
        let storage1 = cr;
        let storage2 = cd;
        if(atk <= 0 || cr <= 2 || cd <= 0){
            interaction.reply("Sucrose Says these stats don't look right, Please check again traveller.");
        }
        else if(cr>100){
                cr = 100
                cr /= 100
				cd /= 100
                var result = (atk*(1 + cr*cd)).toFixed(2);
                interaction.reply(`CV is ${result} - for stats ${atk},100,${storage2}`);
            //interaction.reply("stop listening to akra. You don't need more than 100 crit rate")
        }
        else{
            if(cr > 2){
				cr /= 100
				cd /= 100
            }
            var result = (atk*(1 + cr*cd)).toFixed(2);
            interaction.reply(`CV is ${result} - for stats ${atk},${storage1},${storage2}`);
        }
    }
})
client.on("interactionCreate", (interaction) => {
    if(!interaction.isChatInputCommand()) return;
    // console.log(interaction);
    if(interaction.commandName === 'clear'){
        const value = interaction.options.get('count').value;
        if(value>10){
            interaction.reply("Uhhh too much work T_T, Please try less than 10 messages to delete");
        }
        else if(value<=0){
            interaction.reply("Please try more than 1 message to delete");
        }
        else{
            interaction.channel.bulkDelete(parseInt(value)).then(()=>{
                interaction.reply(`Cleared ${value} messages`).then(msg => msg.delete(500));
            }).catch((err)=>{
                return interaction.reply("An error Occured!");
            });
        }
    }
});
client.login(process.env.TOKEN);
