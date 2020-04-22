from creds import secret, client_id, password, username, pasteBinKey, pasteBinUserKey
import praw
import requests


botComment = None
questions = []
answers = []
message = ""


reddit = praw.Reddit(client_id=client_id,
                     client_secret=secret,
                     password=password,
                     user_agent='amabot by /u/Thravia',
                     username=username)



def scanThread(submission):

    botComment = None

    ##Load all comments (replace "click for more comments" with actual comments)
    while True:
        try:
            submission.comments.replace_more(limit=None)
            break
        except Exception:
            print('Handling replace_more exception')
    
    ## iterate over each 1st level comment (1st level comment = a comment that is not a reply to another comment)
    for top_level_comment in submission.comments.list():

        ## if it has an author object (unless comment is deleted it will have an author object)
        if top_level_comment.author is not None: 

            ##check if the current comment was made by the bot
            if top_level_comment.author.name == username:
                #assign the current comment to botComment variable for later purpose
                botComment = top_level_comment

            ## go over each reply to the current comment
            for reply in top_level_comment.replies:

                ## if author of this comment reply is the author of the submission
                ## we consider it an answer to a questions
                if reply.author == submission.author:

                    ## push the entire comment into our answers list
                    answers.append(reply.body)
                    ## push the parent comment (ie. the question) to our questions list
                    questions.append(top_level_comment.body)

    ## generate a long string which matches questions with answers
    post = buildMessage(questions, answers, message)
    ## post our string as a comment / or edit our existing comment with the string
    postToReddit(botComment, submission, post)


def buildMessage(questions, answers, message):

    for q in range(len(questions)):
        message = message + "Question: " + questions[q] + "\n\n" + "Answer: " + answers[q] +"\n\n"
        ##seperate questions
        message = message + "----" + "\n"
    return message


def postToReddit(botComment, submission, message):

    introduction = "I found {0} question(s) and {1} answer(s).\n\n".format(len(questions), len(answers))

    ## if the length of our message is more than 9900 characters
    ## it cannot fit in one comment
    if len(message) > 9900:
        print("message too long, making pastebin link")
        return
        ## upload our message to pastebin and retrieve url for that paste
        pastebinlink = toPasteBin(message, submission.url)
        ## set our message to be just our introduction string + our pastebin link
        message = introduction + "There are too many questions to put in one comment, so I uploaded them with their answers to " + pastebinlink + "----"
    else:
        message = introduction + message

    ## add bot signature
    message = message + "\n *I am a bot. If I am being naughty please contact my owner /u/Thravia*"
    ## if bot already has a comment in this thread
    if botComment is not None:
        ##print("found my own comment")
        botComment.edit(message)
    else:
        ##print("didnt find my own comment")
        submission.reply(message)


def toPasteBin(text, name):
    postURL = "https://pastebin.com/api/api_post.php"
    header = {"charset":"utf-8"}
    params = {
        "api_dev_key": pasteBinKey,
        "api_option": "paste",
        "api_paste_code": text,
        "api_paste_name": name,
    }

    req = requests.post(postURL, data=params, headers=header)
    print(req.status_code, req.text)
    return req.text



def printResults(questions, answers):
    for q in range(len(questions)):
            print("question: " + questions[q])
            print("\n")
            print("answer: " + answers[q])
            print("----------------------")
            print("\n")


##scanThread(submissionId, message)


