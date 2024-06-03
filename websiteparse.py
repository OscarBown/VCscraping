from groq import Groq

client = Groq()

#open webscraping file
with open('scrapedtext.txt', 'r') as scrapedtext:
    text = scrapedtext.read()

#Call in the LLama3 model and ask it my prompt
completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": "extract the: company name, description, stage of investment, date of investment & Location from this copy and paste of a venture capital website:" + text + ". note that not all information may be there." +
            "Since the data is from a website, note that the start and end of the file will be useless (e.g. website titles and contact information). Please then filter for companies who are: based in the UK, NOT to do with health & received funding post 2019. please still give me their descriptions"
        },
    ],
    temperature=0.1,
    max_tokens=4096,
    top_p=0.2,
    stream=True,
    stop=None,
)

#save output to a markdown file
output_file_name = f"parsedwebsite.md"
with open(output_file_name, 'w') as output_file:
    for chunk in completion:
        output_file.write(chunk.choices[0].delta.content or "")
    print("file saved")
