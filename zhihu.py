import time
from pyppeteer import launch
from pyquery import PyQuery as pq 
import asyncio
import pandas

async def run():
    "主函数用来运行程序流程"
    browser = await launch(options={'args': ['--no-sandbox']})
    page = await browser.newPage()
    await page.goto('https://www.zhihu.com/topics')
    await page.waitForSelector('.zm-topic-cat-main')
    result = []
    topics = []
    doc = pq(await page.content())
    for item in doc('.zm-topic-cat-main').items():
        topic_name = item.text()
        master_topic =topic_name
        topics.append(master_topic)
    await page.close()
    topic  = await browser.newPage()
    for topic_name in topics:
        await topic.goto("https://www.zhihu.com/topics#"+topic_name)
        click_continue = True
        while click_continue:
            try:
                # time.sleep(3)
                await topic.waitForSelector('.zg-btn-white')
                # await asyncio.wait(
                #     page.waitForNavigation(),
                #     topic.click('.zg-btn-white',options={'clickCount':1}) ,
                # )
                await topic.evaluate('window.scrollBy(0, window.innerHeight)')
            except Exception as e:
                click_continue = False

        await topic.waitForSelector('.blk')
        doc = pq(await topic.content())
        names = {item.text():item.attr('href') for item in doc('.blk a').items() if "topic" in item.attr("href")}
        #tab = await browser.newPage()
        # for key,value in names.items():
        #     topic_message =  [] 
        #     topic_message.append(topic_name)
        #     topic_message.append(key)
        #     topic_message.append(value)
        #     await tab.goto(f"https://www.zhihu.com{value}/hot")
        #     await tab.waitForSelector('.NumberBoard-itemValue')
        #     people_doc = pq(await tab.content())
        #     await tab.close(runBeforeUnload=True)

        #     nums = people_doc('.NumberBoard-itemValue').text()
        #     topic_message.append(nums.split()[0])
        #     topic_message.append(nums.split()[1])
        #     result.append(topic_message)

        #     await asyncio.sleep(3)    
    await topic.close()
    await browser.close()
    df = pandas.DataFrame(result)
    df.to_excel('output.xls',columns={'0':"大主题",'1':'小主题','2':'小主题连接',3:'关注人数',4:'问题数'})




if __name__ == "__main__":
    asyncio.run(  run())
  