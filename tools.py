import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
from typing import List, Dict, Optional
import re
import base64
import os

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

def get_weather(location: str, lang: str = "zh") -> str:
    """
    获取指定城市的实时天气信息
    :param location: 城市名称（支持中文、英文）
    :param lang: 语言代码，默认 'zh' 中文
    :return: 格式化的天气信息
    """
    try:
        # 方案1: 使用 wttr.in API（无需密钥）
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }
        
        # wttr.in 支持多语言和 JSON 格式
        url = f"https://wttr.in/{urllib.parse.quote(location)}?format=j1&lang={lang}"
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # 提取当前天气信息
            current = data.get("current_condition", [{}])[0]
            weather_desc = current.get("lang_zh", [{}])[0].get("value", "") if lang == "zh" else current.get("weatherDesc", [{}])[0].get("value", "")
            if not weather_desc and lang == "zh":
                # 如果没有中文描述，使用英文并翻译常见天气
                weather_desc = current.get("weatherDesc", [{}])[0].get("value", "")
                weather_desc = translate_weather(weather_desc)
            
            temp_c = current.get("temp_C", "N/A")
            feels_like_c = current.get("FeelsLikeC", "N/A")
            humidity = current.get("humidity", "N/A")
            wind_speed = current.get("windspeedKmph", "N/A")
            wind_dir = current.get("winddir16Point", "N/A")
            pressure = current.get("pressure", "N/A")
            visibility = current.get("visibility", "N/A")
            
            # 获取今日天气预报
            today_weather = data.get("weather", [{}])[0]
            max_temp = today_weather.get("maxtempC", "N/A")
            min_temp = today_weather.get("mintempC", "N/A")
            
            # 获取降水概率
            hourly = today_weather.get("hourly", [])
            if hourly:
                rain_chances = [int(h.get("chanceofrain", 0)) for h in hourly]
                avg_rain_chance = sum(rain_chances) // len(rain_chances) if rain_chances else 0
            else:
                avg_rain_chance = 0
            
            # 格式化输出
            result = f"""**{location}实时天气**
当前时间：{data.get("current_condition", [{}])[0].get("localObsDateTime", "未知")}

🌡️ **温度**：{temp_c}°C（体感 {feels_like_c}°C）
🌤️ **天气**：{weather_desc}
💨 **风况**：{translate_wind_dir(wind_dir)} {wind_speed} km/h
💧 **湿度**：{humidity}%
🌧️ **降水概率**：{avg_rain_chance}%
📊 **气压**：{pressure} hPa
👁️ **能见度**：{visibility} km

📅 **今日预报**
最高温度：{max_temp}°C
最低温度：{min_temp}°C

数据来源：wttr.in"""
            
            return result
            
        else:
            # 如果 wttr.in 失败，使用备用方案
            return search_weather_fallback(location)
            
    except Exception as e:
        # 发生错误时使用备用方案
        return search_weather_fallback(location)

def translate_weather(weather_en: str) -> str:
    """翻译常见天气描述"""
    translations = {
        "Clear": "晴",
        "Sunny": "晴",
        "Partly cloudy": "多云",
        "Cloudy": "阴",
        "Overcast": "阴天",
        "Mist": "薄雾",
        "Patchy rain possible": "局部可能有雨",
        "Patchy snow possible": "局部可能有雪",
        "Patchy sleet possible": "局部可能有雨夹雪",
        "Thundery outbreaks possible": "可能有雷暴",
        "Blowing snow": "风雪",
        "Blizzard": "暴风雪",
        "Fog": "雾",
        "Freezing fog": "冻雾",
        "Patchy light drizzle": "局部小雨",
        "Light drizzle": "小雨",
        "Heavy rain": "大雨",
        "Light rain": "小雨",
        "Moderate rain": "中雨",
        "Heavy snow": "大雪",
        "Light snow": "小雪",
        "Moderate snow": "中雪"
    }
    return translations.get(weather_en, weather_en)

def translate_wind_dir(wind_dir: str) -> str:
    """翻译风向"""
    translations = {
        "N": "北风",
        "NNE": "东北偏北风",
        "NE": "东北风",
        "ENE": "东北偏东风",
        "E": "东风",
        "ESE": "东南偏东风",
        "SE": "东南风",
        "SSE": "东南偏南风",
        "S": "南风",
        "SSW": "西南偏南风",
        "SW": "西南风",
        "WSW": "西南偏西风",
        "W": "西风",
        "WNW": "西北偏西风",
        "NW": "西北风",
        "NNW": "西北偏北风"
    }
    return translations.get(wind_dir, wind_dir)

def search_weather_fallback(location: str) -> str:
    """备用天气搜索方案：通过 DuckDuckGo 搜索天气信息"""
    try:
        # 使用 DuckDuckGo 搜索天气
        search_query = f"{location} 天气 实时"
        encoded_query = urllib.parse.quote(search_query)
        
        # DuckDuckGo 有一个特殊的天气查询端点
        url = f"https://duckduckgo.com/?q={encoded_query}&ia=weather"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尝试提取天气信息
        weather_module = soup.find('div', class_='module--weather')
        if weather_module:
            # 提取温度
            temp_elem = weather_module.find('span', class_='module__temperature')
            temp = temp_elem.text.strip() if temp_elem else "未知"
            
            # 提取天气描述
            desc_elem = weather_module.find('div', class_='module__weather-type')
            weather_desc = desc_elem.text.strip() if desc_elem else "未知"
            
            # 提取其他信息
            details = weather_module.find_all('span', class_='module__weather-detail')
            detail_text = " | ".join([d.text.strip() for d in details]) if details else ""
            
            return f"""**{location}天气信息**（来源：DuckDuckGo）

🌡️ 温度：{temp}
🌤️ 天气：{weather_desc}
📊 其他信息：{detail_text}

提示：由于使用了搜索引擎数据，信息可能不够完整。建议访问专业天气网站获取更详细信息。"""
        
        # 如果没有找到天气模块，尝试通用搜索
        return f"""未能获取 {location} 的实时天气数据。

建议您通过以下方式查询：
1. 访问中国天气网：http://www.weather.com.cn
2. 使用手机自带天气应用
3. 搜索"{location}天气"获取最新信息

技术提示：天气API暂时无法访问，请稍后再试。"""
        
    except Exception as e:
        return f"获取天气信息时出错：{str(e)}\n\n请尝试直接访问天气网站查询。"

def open_web_page(url: str, action: str = "screenshot") -> str:
    """
    打开网页并执行操作（截图、获取内容等）
    集成 MCP browser-tools 服务器功能
    :param url: 要打开的网页URL
    :param action: 操作类型 ("screenshot", "content", "logs")
    :return: 操作结果
    """
    try:
        # 首先尝试使用 MCP browser-tools 服务器
        try:
            # 导入 MCP 工具（如果可用）
            from use_mcp_tool import use_mcp_tool
            
            # 使用 MCP browser-tools 服务器截图
            if action == "screenshot":
                result = use_mcp_tool(
                    "github.com/AgentDeskAI/browser-tools-mcp",
                    "takeScreenshot",
                    {}
                )
                
                if "成功" in str(result) or "success" in str(result).lower():
                    return f"✅ 网页截图成功\n网址：{url}\n结果：{result}"
                else:
                    # 如果截图失败，尝试备用方案
                    return open_web_page_fallback(url, action)
            
            elif action == "logs":
                console_logs = use_mcp_tool(
                    "github.com/AgentDeskAI/browser-tools-mcp",
                    "getConsoleLogs",
                    {}
                )
                return f"📋 浏览器控制台日志\n网址：{url}\n日志：{console_logs}"
            
            elif action == "content":
                # 先截图，然后获取内容
                screenshot_result = use_mcp_tool(
                    "github.com/AgentDeskAI/browser-tools-mcp",
                    "takeScreenshot", 
                    {}
                )
                return f"📄 网页内容获取\n网址：{url}\n截图：{screenshot_result}\n\n内容：{extract_webpage_content(url)}"
                
        except ImportError:
            # 如果 MCP 不可用，使用备用方案
            return open_web_page_fallback(url, action)
        except Exception as mcp_error:
            print(f"MCP browser-tools 调用失败: {mcp_error}")
            return open_web_page_fallback(url, action)
            
    except Exception as e:
        return f"❌ 打开网页失败：{str(e)}"

def open_web_page_fallback(url: str, action: str = "screenshot") -> str:
    """
    备用网页访问方案：使用 requests + BeautifulSoup
    :param url: 网页URL
    :param action: 操作类型
    :return: 操作结果
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        if action == "content":
            # 提取并返回页面内容
            content = extract_webpage_content(url, max_length=2000)
            return f"📄 网页内容获取成功\n{content}"
            
        elif action == "screenshot":
            # 无法真正截图，但可以返回页面基本信息
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "无标题"
            
            # 获取页面基本信息
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '无描述') if meta_desc else "无描述"
            
            # 统计页面元素
            links_count = len(soup.find_all('a'))
            images_count = len(soup.find_all('img'))
            
            return f"""📱 网页访问成功（备用模式）
网址：{url}
标题：{title_text}
描述：{description}
状态：{response.status_code} - 页面正常加载
元素统计：{links_count} 个链接，{images_count} 张图片

⚠️ 注意：当前使用备用模式，无法提供真实截图。
如需完整浏览器功能，请确保 MCP browser-tools 服务器正常运行。"""
            
        elif action == "logs":
            return f"""📋 网页访问日志（备用模式）
网址：{url}
HTTP状态：{response.status_code}
响应头：{dict(list(response.headers.items())[:5])}
页面大小：{len(response.text)} 字符

⚠️ 注意：当前使用备用模式，无法获取浏览器控制台日志。"""
            
    except requests.RequestException as e:
        return f"❌ 网页访问失败：{str(e)}"
    except Exception as e:
        return f"❌ 处理网页时出错：{str(e)}"
