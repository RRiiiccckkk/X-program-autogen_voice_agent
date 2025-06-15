import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
from typing import List, Dict, Optional
import re

def search_duckduckgo(query: str, max_results: int = 3) -> str:
    """
    使用 DuckDuckGo 搜索（无需 API 密钥）
    :param query: 搜索查询
    :param max_results: 最大结果数
    :return: 搜索结果的格式化字符串
    """
    try:
        # DuckDuckGo HTML 搜索
        encoded_query = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        # 查找搜索结果
        result_links = soup.find_all('a', class_='result__a')[:max_results]
        
        for i, link in enumerate(result_links, 1):
            title = link.get_text(strip=True)
            href = link.get('href', '')
            
            # 获取描述文本
            parent = link.find_parent('div', class_='results_links')
            snippet = ""
            if parent:
                snippet_elem = parent.find('a', class_='result__snippet')
                if snippet_elem:
                    snippet = snippet_elem.get_text(strip=True)
            
            results.append(f"{i}. **{title}**\n   {snippet}\n   链接: {href}")
        
        if results:
            return f"DuckDuckGo 搜索结果 '{query}':\n\n" + "\n\n".join(results)
        else:
            return f"未找到关于 '{query}' 的搜索结果。"
            
    except Exception as e:
        return f"DuckDuckGo 搜索出错: {str(e)}"

def search_wikipedia(query: str, language: str = "zh") -> str:
    """
    搜索维基百科
    :param query: 搜索查询
    :param language: 语言代码（zh=中文, en=英文）
    :return: 维基百科摘要
    """
    try:
        # 维基百科 API
        api_url = f"https://{language}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
        headers = {"User-Agent": "MultiAgentBot/1.0"}
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            title = data.get('title', query)
            extract = data.get('extract', '未找到摘要')
            
            result = f"**维基百科: {title}**\n\n{extract}"
            
            # 如果有相关链接
            if 'content_urls' in data:
                desktop_url = data['content_urls']['desktop']['page']
                result += f"\n\n更多信息: {desktop_url}"
                
            return result
        else:
            # 如果没有找到，尝试搜索
            search_url = f"https://{language}.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'list': 'search',
                'srsearch': query,
                'format': 'json',
                'srlimit': 1
            }
            
            search_response = requests.get(search_url, params=params, headers=headers, timeout=10)
            if search_response.status_code == 200:
                search_data = search_response.json()
                if search_data['query']['search']:
                    first_result = search_data['query']['search'][0]
                    return search_wikipedia(first_result['title'], language)
            
            return f"未在维基百科找到关于 '{query}' 的条目。"
            
    except Exception as e:
        return f"维基百科搜索出错: {str(e)}"

def extract_webpage_content(url: str, max_length: int = 1000) -> str:
    """
    提取网页的主要内容
    :param url: 网页 URL
    :param max_length: 最大内容长度
    :return: 提取的内容
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 移除脚本和样式
        for script in soup(["script", "style"]):
            script.decompose()
        
        # 尝试找到主要内容区域
        content_areas = soup.find_all(['article', 'main', 'div'], class_=re.compile('content|article|main|body'))
        
        if content_areas:
            text = ' '.join([area.get_text(separator=' ', strip=True) for area in content_areas])
        else:
            # 如果没有找到特定区域，获取所有段落
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50])
        
        # 清理文本
        text = re.sub(r'\s+', ' ', text)
        text = text[:max_length] + "..." if len(text) > max_length else text
        
        return f"网页内容摘要 ({url}):\n\n{text}"
        
    except Exception as e:
        return f"无法提取网页内容: {str(e)}"

def search_web(query: str) -> str:
    """
    综合网络搜索功能，尝试多个搜索源
    :param query: The search query.
    :return: The content of the top search result.
    """
    results = []
    
    # 1. 尝试 DuckDuckGo 搜索
    ddg_result = search_duckduckgo(query, max_results=2)
    if "搜索结果" in ddg_result:
        results.append(ddg_result)
    
    # 2. 尝试维基百科（如果查询看起来像是寻找定义或解释）
    if any(keyword in query.lower() for keyword in ['是什么', '什么是', '定义', '介绍', 'what is', 'define']):
        wiki_result = search_wikipedia(query)
        if "维基百科" in wiki_result:
            results.append(wiki_result)
    
    # 3. 如果有结果，返回组合结果
    if results:
        return "\n\n---\n\n".join(results)
    else:
        return f"未能找到关于 '{query}' 的相关信息。请尝试更改搜索词或使用更具体的查询。"

def search_news(query: str) -> str:
    """
    搜索最新新闻（使用 Google News RSS）
    :param query: 新闻查询
    :return: 新闻结果
    """
    try:
        # Google News RSS (无需 API)
        encoded_query = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
        
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'xml')
        
        items = soup.find_all('item')[:5]  # 获取前5条新闻
        
        if not items:
            return f"未找到关于 '{query}' 的新闻。"
        
        news_results = [f"最新新闻关于 '{query}':\n"]
        
        for i, item in enumerate(items, 1):
            title = item.find('title').text if item.find('title') else "无标题"
            pub_date = item.find('pubDate').text if item.find('pubDate') else "日期未知"
            link = item.find('link').text if item.find('link') else "#"
            
            # 简化日期格式
            try:
                from datetime import datetime
                date_obj = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z')
                pub_date = date_obj.strftime('%Y-%m-%d %H:%M')
            except:
                pass
            
            news_results.append(f"{i}. **{title}**\n   发布时间: {pub_date}\n   链接: {link}")
        
        return "\n\n".join(news_results)
        
    except Exception as e:
        return f"新闻搜索出错: {str(e)}"

def get_exchange_rate(base_currency: str, target_currency: str) -> str:
    """
    Get the exchange rate between two currencies.
    :param base_currency: The base currency (e.g., "USD").
    :param target_currency: The target currency (e.g., "CNY").
    :return: The exchange rate as a string.
    """
    url = f"https://open.er-api.com/v6/latest/{base_currency}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and 'rates' in data:
            exchange_rate = data['rates'].get(target_currency)
            if exchange_rate:
                return f"The exchange rate from {base_currency} to {target_currency} is: {exchange_rate}"
            else:
                return f"Could not retrieve the exchange rate for {target_currency}."
        else:
            return f"Error fetching exchange rates: {data.get('error-type', 'Unknown error')}"
    except Exception as e:
        return f"An error occurred: {e}"
