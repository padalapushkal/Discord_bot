require('dotenv').config();
const {REST, Routes, ApplicationCommandOptionType } = require('discord.js')

const commands = [
    {
        name : 'sayhello',
        description : 'Sucorse replies hello to traveller',
    },
    {
        name : 'sayloveyou',
        description : 'Sucrose tells I love you',
        options : [
            {
                name : 'person-name',
                description : 'Please Enter the @name of person you want to send the message to',
                type : ApplicationCommandOptionType.String,
                required : true,
            },
        ],
    },
    {
        name : 'aboutme',
        description : 'Sucrose tells more details about herself'
    },
    {
        name : 'clear',
        description : 'Sucrose uses alchemy jutsu to clear the past messages in server',
        options : [
            {
                name : 'count',
                description : 'Enter the number of messages to delete',
                type : ApplicationCommandOptionType.Number,
                required : true,
            },
        ],
    },
    {
        name : 'artifact_value',
        description : "Sucrose will judge your artifact CV",
        options : [
            {
                name : 'main-stat', 
                description : 'Main Stat Should be the Max Atk/Def/Hp based on character scalings',
                type : ApplicationCommandOptionType.Number,
                required : true
            },
            {
                name : 'crit-rate',
                description : 'Enter the Crit rate here',
                type : ApplicationCommandOptionType.Number,
                required : true,
            },
            {
                name : 'crit-damage',
                description : "Enter the Crit Damage here",
                type : ApplicationCommandOptionType.Number,
                required : true,
            },
        ],
    },
]; // I died a little here name should not be capital 
const rest = new REST({ version: '10'}).setToken(process.env.TOKEN);

(async () => {
    try{
        console.log('Registering the commands into discord');
        await rest.put(
            Routes.applicationGuildCommands(process.env.CLIENT_ID, process.env.GUILD_ID), 
            {
                body : commands
            }
        )
        console.log('Slash commands were registered');
    }
    catch(error){
        console.log(`There was an error : ${error}`);
    }
})();