# import networkx as nx
# import matplotlib.pyplot as plt
# from matplotlib.colors import LinearSegmentedColormap

# class InteractionGraph:
#     def __init__(self):
#         self.G = nx.DiGraph()  # Используем ориентированный граф
        
#     def add_interaction(self, speaker, addressee, tone=None):
#         if self.G.has_edge(speaker, addressee):
#             self.G[speaker][addressee]["weight"] += 1
#             if tone:
#                 self.G[speaker][addressee]["tones"].append(tone)
#         else:
#             self.G.add_edge(speaker, addressee, weight=1, tones=[tone] if tone else [])

#     def visualize(self, filename="social_graph.png"):
#         plt.figure(figsize=(14, 10))
        
#         # Создаем позиции узлов
#         pos = nx.spring_layout(self.G, k=0.8, seed=42)
        
#         # Настраиваем цвета
#         cmap = LinearSegmentedColormap.from_list("tone_cmap", ["#4e79a7", "#f28e2b", "#e15759"])
        
#         # Рисуем узлы
#         nx.draw_networkx_nodes(
#             self.G, pos, 
#             node_size=2500,
#             node_color="#76b7b2",
#             alpha=0.9
#         )
        
#         # Рисуем ребра с учетом весов и тонов
#         edges = self.G.edges(data=True)
#         edge_colors = []
#         edge_widths = []
        
#         for u, v, d in edges:
#             edge_widths.append(d['weight'] * 1.5)
#             if d['tones']:
#                 # Средний тон по цветовой шкале
#                 edge_colors.append(cmap(len(d['tones'])/5))
#             else:
#                 edge_colors.append("#bab0ac")
        
#         nx.draw_networkx_edges(
#             self.G, pos,
#             edgelist=edges,
#             width=edge_widths,
#             edge_color=edge_colors,
#             alpha=0.7,
#             arrowstyle='->',
#             arrowsize=20
#         )
        
#         # Подписи и легенда
#         nx.draw_networkx_labels(self.G, pos, font_size=12, font_weight='bold')
        
#         # Добавляем информацию о взаимодействиях
#         edge_labels = {(u, v): f"{d['weight']}x" for u, v, d in edges}
#         nx.draw_networkx_edge_labels(
#             self.G, pos,
#             edge_labels=edge_labels,
#             font_size=10
#         )
        
#         plt.title("Динамика социальных взаимодействий", fontsize=16, pad=20)
#         plt.axis('off')
        
#         # Сохраняем с высоким DPI
#         plt.savefig(filename, dpi=300, bbox_inches='tight')
#         plt.close()
        
#         return filename

from typing import Optional, Dict, List, Tuple
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class InteractionGraph:
    def __init__(self):
        """Инициализация графа с поддержкой эмоциональной окраски"""
        self.G = nx.DiGraph()  # Ориентированный граф для учета направления взаимодействий
        self.emotion_data = {}  # {(from, to): {'count': int, 'sentiments': list}}
        self._configure_style()

    def add_interaction(self, source: str, target: Optional[str], sentiment: float, comm_type: str):
        """
        Добавляет взаимодействие с указанием типа
        :param target: None для публичных сообщений
        """
        if comm_type == "public":
            target = "ALL"  # Специальное значение для публичных сообщений
    
        key = (source, target)
    
        if key not in self.emotion_data:
            self.emotion_data[key] = {'count': 0, 'sentiments': [], 'types': []}
    
        self.emotion_data[key]['count'] += 1
        self.emotion_data[key]['sentiments'].append(sentiment)
        self.emotion_data[key]['types'].append(comm_type)

    def _configure_style(self):
        """Настройка стиля визуализации"""
        # Кастомная цветовая карта: красный-нейтральный-зеленый
        self.cmap = LinearSegmentedColormap.from_list(
            'emotion_cmap', ['#ff3333', '#ffff99', '#33cc33'])
        
        self.style = {
            'node_size': 3000,
            'font_size': 12,
            'base_edge_width': 3,
            'figsize': (14, 10),
            'layout': nx.spring_layout,
            'layout_kwargs': {'k': 0.6, 'seed': 42, 'iterations': 100},
            'arrow_size': 20
        }

    def add_interaction(self, source: str, target: str, sentiment: float, comm_type: str):
        """
        Добавляет взаимодействие с указанием типа
        :param source: Отправитель
        :param target: Получатель ("ALL" для публичных)
        :param sentiment: Оценка тональности (-1 до 1)
        :param comm_type: Тип коммуникации ('public' или 'private')
        """
        key = (source, target)
        
        if key not in self.emotion_data:
            self.emotion_data[key] = {'count': 0, 'sentiments': [], 'types': []}
        
        self.emotion_data[key]['count'] += 1
        self.emotion_data[key]['sentiments'].append(sentiment)
        self.emotion_data[key]['types'].append(comm_type)
        
        if self.G.has_edge(source, target):
            self.G[source][target]['weight'] += 1
        else:
            self.G.add_edge(source, target, weight=1, type=comm_type)


    def _calculate_edge_properties(self):
        """Вычисляет свойства ребер для визуализации"""
        edge_data = []
        for (source, target), data in self.emotion_data.items():
            count = data['count']
            avg_sentiment = np.mean(data['sentiments'])
            edge_data.append((
                source, target,
                {
                    'width': count * self.style['base_edge_width'],
                    'color': self._sentiment_to_color(avg_sentiment),
                    'alpha': min(0.3 + count*0.1, 0.9),
                    'label': f"{count}\n({avg_sentiment:.2f})",
                    'avg_sentiment': avg_sentiment
                }
            ))
        return edge_data

    def _sentiment_to_color(self, sentiment: float) -> str:
        """Преобразует оценку тональности в цвет"""
        # Нормализуем от -1..1 к 0..1
        norm = (sentiment + 1) / 2
        return self.cmap(norm)

    def visualize(self, filename: str = "social_graph.png"):
        """Визуализирует граф с эмоциональной окраской"""
        plt.figure(figsize=self.style['figsize'])
        pos = self.style['layout'](self.G, **self.style['layout_kwargs'])
        edge_data = self._calculate_edge_properties()

        # Рисуем узлы
        nx.draw_networkx_nodes(
            self.G, pos,
            node_size=self.style['node_size'],
            node_color='#1f78b4',
            alpha=0.8
        )

        # Рисуем ребра с разными стилями для разных типов
        for edge in self.G.edges(data=True):
            edge_type = edge[2].get('type', 'private')
            edge_style = 'dashed' if edge_type == 'private' else 'solid'
            nx.draw_networkx_edges(
                self.G, pos,
                edgelist=[(edge[0], edge[1])],
                width=2,
                edge_color='#888888',
                alpha=0.7,
                style=edge_style
            )


        # Подписи узлов
        nx.draw_networkx_labels(
            self.G, pos,
            font_size=self.style['font_size'],
            font_weight='bold',
            font_color='white'
        )

        # Подписи ребер (количество + средняя тональность)
        edge_labels = {(src, tgt): props['label'] for src, tgt, props in edge_data}
        nx.draw_networkx_edge_labels(
            self.G, pos,
            edge_labels=edge_labels,
            font_size=9,
            bbox=dict(alpha=0.7)
        )

        # Легенда для цветов
        self._add_colorbar()

        plt.title("Социальные взаимодействия с эмоциональной окраской", fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

    def _add_colorbar(self):
        """Добавляет цветовую шкалу для интерпретации"""
        sm = plt.cm.ScalarMappable(
            cmap=self.cmap,
            norm=plt.Normalize(vmin=-1, vmax=1))
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=plt.gca(), shrink=0.7)
        cbar.set_label('Эмоциональная окраска взаимодействий', rotation=270, labelpad=20)
        cbar.set_ticks([-1, 0, 1])
        cbar.set_ticklabels(['Негатив', 'Нейтрально', 'Позитив'])