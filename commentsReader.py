
#Authors: Aryan Ershadi & Louai Rahal

import googleapiclient.discovery
import pandas as pd

def main():

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "......"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)


    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=".....",
        maxResults = 100,
        textFormat = "plainText"
    )
   
    response = request.execute()


    data = {
        "Comment": [],
        "Type": [],
        "Number of Likes": [],
        "Date Posted": [],
        "Number of Replies": []
    }

    #load data into a DataFrame object:
    df = pd.DataFrame(data)
    
    for item in response["items"]:
        i = item["snippet"]["topLevelComment"]
        s= i["snippet"]["textDisplay"]
        nlikes = i["snippet"]["likeCount"]
        date = i["snippet"]["publishedAt"]
        nreplies = item["snippet"]["totalReplyCount"]
        pid = item["id"]
        
        df.loc[len(df)] = [s,'topLevelComment',nlikes, date, nreplies]         
        
        if "replies" in item:
            request2 = youtube.comments().list(
                part = "snippet",
                maxResults=100,
                parentId=pid,
                textFormat="plainText"
            )
            response2 = request2.execute()
            for i in response2["items"]:
                nlikes = i["snippet"]["likeCount"]
                date = i["snippet"]["publishedAt"]
                s = i["snippet"]["textDisplay"]
                df.loc[len(df)] = [s,'reply',nlikes, date, 0]
	    
    
    while("nextPageToken" in response):

        tk = response["nextPageToken"]
        
        request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId="....",
        maxResults = 100,
        pageToken = tk,
        textFormat = "plainText"

        )
   
        response = request.execute()

        for item in response["items"]:
            i = item["snippet"]["topLevelComment"]
            s= i["snippet"]["textDisplay"]
            nlikes = i["snippet"]["likeCount"]
            date = i["snippet"]["publishedAt"]
            nreplies = item["snippet"]["totalReplyCount"]
            pid = item["id"]
        
            df.loc[len(df)] = [s,'topLevelComment',nlikes, date, nreplies]         
        
            if "replies" in item:
                request3 = youtube.comments().list(
                part = "snippet",
                maxResults=100,
                parentId=pid,
                textFormat="plainText"
                )
                response3 = request3.execute()
                for i in response3["items"]:
                    nlikes = i["snippet"]["likeCount"]
                    date = i["snippet"]["publishedAt"]
                    s = i["snippet"]["textDisplay"]
                    df.loc[len(df)] = [s,'reply',nlikes, date, 0]

    
    df.to_excel("output.xlsx")   

if __name__ == "__main__":
    main()
