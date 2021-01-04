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
        topics = str(topic_name).split('\n')
        #topics.append(master_topic)
    await page.close()
    writer = pandas.ExcelWriter('output.xlsx')
    topic  = await browser.newPage()
    for topic_name in topics:
        print('=========topic_name',topic_name,'len',len(topics))
        await topic.goto("https://www.zhihu.com/topics#"+topic_name)
        click_continue = True
        while click_continue:
            try:
                await topic.waitForSelector('.zg-btn-white')
                await topic.click('.zg-btn-white',options={'clickCount':1})
                # await asyncio.gather(
                #     topic.waitForNavigation(),
                #     topic.click('.zg-btn-white',options={'clickCount':1}) ,
                # )
                doc = pq(await topic.content())
                names = {item.text():item.attr('href') for item in doc('.blk a').items() if "topic" in item.attr("href")}
                #await topic.evaluate('window.scrollBy(0, window.innerHeight)')
            except Exception as e:
                click_continue = False

        await topic.waitForSelector('.blk')
        doc = pq(await topic.content())
        names = {item.text():item.attr('href') for item in doc('.blk a').items() if "topic" in item.attr("href")}
        tab = await browser.newPage()
        print(f"==============={names}")
        for key,value in names.items():
            try:
                topic_message =  [] 
                topic_message.append(topic_name)
                topic_message.append(key)
                topic_message.append(value)
                await tab.goto(f"https://www.zhihu.com{value}/hot")
                await tab.waitForSelector('.NumberBoard-itemValue')
                people_doc = pq(await tab.content())
                #await tab.close(runBeforeUnload=True)
                nums = people_doc('.NumberBoard-itemValue').text()
                print(key,value)
                topic_message.append(nums.split()[0])
                topic_message.append(nums.split()[1])
                result.append(topic_message)
            except Exception as e:
                pass
        df1 = pandas.DataFrame(result)
        df1.to_excel(writer,topic_name)
    writer.save()
    await topic.close()
    await browser.close()




if __name__ == "__main__":
    asyncio.run(  run())
  