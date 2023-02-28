from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from pprint import pprint
import random 
from string import Template
import pickle

def scrape_phyorg():
    link1 = "https://phys.org/tags/computer+science/"
    treq = Request(link1, 
    headers={'User-Agent': 'Mozilla/5.0'}
)
    phyorg_webpage = urlopen(treq).read()
    phyorg_webpage_soup = soup(phyorg_webpage,'html.parser')
    soup_titles_ls = phyorg_webpage_soup.find_all('h3',{'class':'mb-1 mb-lg-2'})
    title_ls = []
    for i in soup_titles_ls:
        title_ls.append(i.text)
    soup_sdesc_ls = phyorg_webpage_soup.find_all('p',{'class':'mb-1 pr-1'})
    sdesc_ls = []
    for i in soup_sdesc_ls:
        sdesc_ls.append((i.text).strip())
    phyorg_title_desc_dict = dict(zip(title_ls,sdesc_ls))
    blog_hyperlinks = phyorg_webpage_soup.find_all('div',{'class':'sorted-article-content d-flex flex-column ie-flex-1'})
    blog_hyperlinks_ls = []
    for text in blog_hyperlinks:
        links = text.find_all('a')
        for text in links:
            hrefText = (text['href'])
            blog_hyperlinks_ls.append(hrefText)
    phyorg_title_href_dict = dict(zip(title_ls,blog_hyperlinks_ls))
    return phyorg_title_desc_dict,phyorg_title_href_dict

def scrape_techxplore():
    link3 = "https://techxplore.com/computer-sciences-news/"
    treq = Request(link3, 
    headers={'User-Agent': 'Mozilla/5.0'}
    )
    techxplore_webpage = urlopen(treq).read()
    techxplore_webpage_soup = soup(techxplore_webpage,'html.parser')
    soup_titles_ls = techxplore_webpage_soup.find_all('h2',{'class':'text-middle mb-3'})
    title_ls = []
    for i in soup_titles_ls:
        title_ls.append(i.text)
    soup_sdesc_ls = techxplore_webpage_soup.find_all('p',{'class':'mb-4'})
    sdesc_ls = []
    for i in soup_sdesc_ls:
        sdesc_ls.append((i.text).strip())
    techxplore_title_desc_dict = dict(zip(title_ls,sdesc_ls))
    blog_hyperlinks = techxplore_webpage_soup.find_all('div',{'class':'sorted-article-content d-flex flex-column ie-flex-1'})
    blog_hyperlinks_ls = []
    for text in blog_hyperlinks:
        links = text.find_all('a')
        for text in links:
            hrefText = (text['href'])
            blog_hyperlinks_ls.append(hrefText)
    techxplore_title_href_dict = dict(zip(title_ls,blog_hyperlinks_ls))
    return techxplore_title_desc_dict,techxplore_title_href_dict
    
def scrape_scitech():
    link4 = "https://scitechdaily.com/tag/computer-science/"
    treq = Request(link4, 
    headers={'User-Agent': 'Mozilla/5.0'}
    )
    scitech_webpage = urlopen(treq).read()
    scitech_webpage_soup = soup(scitech_webpage,'html.parser')
    soup_titles_ls = scitech_webpage_soup.find_all('h3',{'class':'entry-title content-list-title'})
    title_ls = []
    for i in soup_titles_ls:
        title_ls.append(i.text)
    soup_sdesc_ls = scitech_webpage_soup.find_all('div',{"class":"content-list-excerpt"})
    sdesc_ls = []
    for i in soup_sdesc_ls:
        sdesc_ls.append((i.text).strip())
    scitech_title_desc_dict = dict(zip(title_ls,sdesc_ls))
    blog_hyperlinks = scitech_webpage_soup.find_all('h3',{'class':'entry-title content-list-title'})
    blog_hyperlinks_ls = []
    for text in blog_hyperlinks:
        links = text.find_all('a')
        for text in links:
            hrefText = (text['href'])
            blog_hyperlinks_ls.append(hrefText)
    scitech_title_href_dict = dict(zip(title_ls,blog_hyperlinks_ls))
    return scitech_title_desc_dict,scitech_title_href_dict

def create_master_record(phyorg_title_desc_dict,techxplore_title_desc_dict,scitech_title_desc_dict,phyorg_title_href_dict,techxplore_title_href_dict,scitech_title_href_dict):
    master_title_sdec_dict = {**phyorg_title_desc_dict,**techxplore_title_desc_dict,**scitech_title_desc_dict}
    master_title_href_dict = {**phyorg_title_href_dict,**techxplore_title_href_dict,**scitech_title_href_dict}
    return master_title_sdec_dict,master_title_href_dict

if __name__=="__main__":
    phyorg_title_desc_dict,phyorg_title_href_dict = scrape_phyorg()
    techxplore_title_desc_dict,techxplore_title_href_dict = scrape_techxplore()
    scitech_title_desc_dict,scitech_title_href_dict = scrape_scitech()
    master_title_sdec_dict,master_title_href_dict = create_master_record(phyorg_title_desc_dict,techxplore_title_desc_dict,scitech_title_desc_dict,phyorg_title_href_dict,techxplore_title_href_dict,scitech_title_href_dict)
    master_title_ls = list(master_title_sdec_dict.keys())
    
    # with open("template/prev_records.pkl",'rb') as fp:
    #     prev_records = pickle.load(fp)
    
    prev_records = []
    master_title_ls = set(master_title_ls)-set(prev_records)
    master_title_ls = list(master_title_ls)
        
    rand_10_titles = random.choices(master_title_ls,k=10)
    pprint(rand_10_titles)
    
    new_prev_records = prev_records + rand_10_titles
    
    with open("template/prev_records.pkl",'wb') as fp:
        pickle.dump(new_prev_records, fp)
    
    with open('template/div.html','r+',encoding='utf-8') as f:
        html_body = f.readlines()
    master_html_body = ""
    html_body = ' '.join([str(char) for char in html_body])
    for i,j in enumerate(rand_10_titles):
        t_html_body = Template(html_body)
        t_html_body = t_html_body.substitute(No=str(i+1),Heading=j,Body=master_title_sdec_dict[j],ArticleLink=master_title_href_dict[j])
        master_html_body+=t_html_body
    
    with open('template/fdiv.html','w',encoding='utf-8') as f:
        f.writelines(master_html_body)
        
    with open(F'template/fdiv.html','r+',encoding='utf-8') as f:
        fdiv = f.readlines()
    fdiv = ' '.join([str(char) for char in fdiv])
        
    with open('template/formatted.html','r+',encoding='utf-8') as f:
        formatted = f.readlines()
    formatted = ' '.join([str(char) for char in formatted])
    
    master_html_body = Template(formatted)
    master_html_body = master_html_body.substitute(Sasi=fdiv,Name='There')
    
    with open('master_body.html','w',encoding='utf-8') as f:
        f.writelines(master_html_body)
        
    
    
        
    
    
 
    
