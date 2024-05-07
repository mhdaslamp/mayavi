import discord
import decouple
import pymysql

from discord.ext import commands


mayavi = commands.Bot(command_prefix="/",intents=discord.Intents.all())




#Wlwcom message
@mayavi.event
async def on_member_join(member):
    welcome_channel = mayavi.get_channel(1236717191408386098)
    message = f"Welcome to the server {member.name}"
    await welcome_channel.send(message)
    await member.send(message)


#sql setup
def fetch_data(query):
    connection = pymysql.connect(host=decouple.config("DB_HOST"),
                                 user=decouple.config("DB_USER"),
                                 password=decouple.config("DB_PASS"),
                                 db=decouple.config("DB"))
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return cursor.fetchall()


#test running
@mayavi.event
async def on_ready():
    print("Bot is running")
    await mayavi.tree.sync()


#inserting words into db
@mayavi.event
async def on_message(message):

    words = message.content.split()

    for word in words:
        word = word.replace("'", "''")
        
        query = f"""INSERT INTO user_words (word,discord_id) VALUES(
            '{word}',
            '{message.author.id}');"""
        fetch_data(query)



#for word count command

@mayavi.tree.command(name="word_count",description="it count the maximum used words")
async def word_count(ctx):
    query = "SELECT word, COUNT(*) as count FROM user_words GROUP BY word ORDER BY count DESC LIMIT 10;"
    result = fetch_data(query)
    response = "Top 10 most used words overall:\n"
    for row in result:
        response += f"{row[0]} - {row[1]} \n"
    await ctx.response.send_message(response)
    


#for user status command

@mayavi.tree.command(name="user_status",description="it count the maximum used words by a specified user")
async def user_status2(ctx, user: discord.User):

    query = f"SELECT word, COUNT(*) AS count FROM user_words WHERE discord_id = '{user.id}' GROUP BY word ORDER BY count DESC LIMIT 10;"
    result = fetch_data(query)



    if not result: 
        response = f"No word usage data found for {user.name}."

    else:
        response = f"Top 10 most used words by {user.name} :\n"
        for row in result:
            response += f"{row[0]} - {row[1]} \n"
        await ctx.response.send_message(response)
    



#for role selection
class  RoleSelection(discord.ui.Select):
    def __init__(self):
        options=[
                discord.SelectOption(label="Moderator",description="moderator of this server"),     
                discord.SelectOption(label="Mulearner",description="mulearner"),  
                discord.SelectOption(label="Student",description="student"),  
                discord.SelectOption(label="Enabler",description="Enabler"),  
        ]

        


        super().__init__(placeholder="Select your Role : ",options=options,min_values=1,max_values=1)




    async def callback(self,interaction: discord.Interaction):

        await interaction.response.send_message(f"You have choosed your role as '{self.values[0]}'")

        async def Adddatatodb(ctx, user: discord.User, selected_role: str):
                
                
                
                query = f"SELECT discord_id FROM user_role;"
                result = fetch_data(query)
                for row in result:
                    print("just printing : ",row)
                    if(row[0] == user.id):
                        print(row)
                        query = "UPDATE user_role SET role = '{self.values[0]}' WHERE user_id = '{user.id}';"
                        fetch_data(query)

                    
                  
                 
               # query = f"""INSERT INTO user_role (discord_id,role) VALUES(
               # '{user.id}',
               # '{self.values[0]}');"""
               # fetch_data(query)
          

        await Adddatatodb(interaction, interaction.user, {self.values[0]})

    
        

                               


class RoleSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RoleSelection())



@mayavi.tree.command(name="select_role",description="Select your role !")
async def role(ctx: commands.Context):
    await ctx.response.send_message("click the dropdown below to select your option",view=RoleSelectionView())
    



  
# Update the role of the user in the database
        



mayavi.run(decouple.config("TOKEN"))




