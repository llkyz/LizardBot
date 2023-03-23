import discord
from discord.ext import commands
import random
from functions import *
import json

def setup(client):
    @client.event
    async def on_message(message):
        if message.channel.type is discord.ChannelType.private:
            prefix = 'DM'
        else:
            prefix = str(message.guild) + " #" + str(message.channel)

            if '<@1032276665092538489>' in message.content and '!battle' not in message.content:
                roll = random.randint(1, 10)
                if roll > 4:
                    await message.channel.send('*slithers by*')
                elif roll == 3:
                    await message.channel.send('*blends into the surroundings*')
                elif roll == 2:
                    await message.channel.send('*munches on some bread*')
                elif roll == 1:
                    await message.reply('*bonks you* <:bonk:687841666182414413>\nYou lost 1 coin!')
                    userData = await fetchUserData(message.author)
                    sql = 'UPDATE userDB SET coins = (coins - 1), userName = %s WHERE userId = %s'
                    val = (message.author.name + "#" + message.author.discriminator, userData["userId"])
                    sqlCursor.execute(sql, val)
                    sqlDb.commit()
        
        #@mod ping
            sqlCursor.execute('SELECT adminPingChannel, adminRoles FROM serverDB WHERE serverId = %s', (message.guild.id,))
            channelData = sqlCursor.fetchone()
            if channelData[0] != None and channelData[1] != None and message.author.id != 1032276665092538489:
                adminPingChannel = message.guild.get_channel(channelData[0])
                adminRoles = json.loads(channelData[1])
                for x in adminRoles:
                    if str(x) in message.content:
                        embed=discord.Embed(title=f"Admin pinged by {message.author.display_name}", description=f"[\[Link\]]({message.jump_url})", color=0x00FF00)
                        embed.set_footer(text=timeNow())
                        await adminPingChannel.send(embed=embed)
                        await message.reply(embed=discord.Embed(title="Mods pinged!", color=0xaacbeb))

            if (message.content.lower().startswith('owo owo') or message.content.lower().startswith('owoowo') or message.content.lower().startswith('owoify')) and client.settings["owo"] and message.author.id != 408785106942164992:
                await message.reply(f'{message.author.mention} used owo owo <:bonk:687841666182414413>')

            # Sunflower dailies
            if (message.content.lower().startswith('owo sunflower <@262909760255426570>')):
                receiverId = message.author.id
                guild = await client.fetch_guild(message.guild.id)
                getUser = await guild.fetch_member(receiverId)
                receiverData = await fetchUserData(getUser)
                
                if receiverData == None:
                    sql = "INSERT INTO userDB (userId, userName, coins, daily) VALUES (%s, %s, %s, %s)"
                    val = (receiverId, getUser.name + "#" + getUser.discriminator, 20000000, "0")
                    sqlCursor.execute(sql, val)

                    await message.reply(f'<:lizard_coin:1047527590677712896> | **{getUser.display_name}** received **{"{:,}".format(20000000)}** coins!')
                else:
                    sqlCursor.execute('SELECT CURDATE()')
                    currentDate = sqlCursor.fetchone()[0]
                    if str(currentDate) != receiverData["daily"]:                        
                        sql = 'UPDATE userDB SET coins = LEAST(coins + %s, 2147483647), daily = %s WHERE userId = %s'
                        val = (20000000,  str(currentDate), receiverId)
                        sqlCursor.execute(sql, val)
                        sqlDb.commit()

                        await message.reply(f'<:lizard_coin:1047527590677712896> | **{getUser.display_name}** received **{"{:,}".format(20000000)}** coins!')

            await client.process_commands(message)

        print(f"[{prefix}] " + str(message.author) + ": " + str(message.content))