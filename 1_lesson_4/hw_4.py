import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LinearRegression



class GradientDescentMse:
    """
    Базовый класс для реализации градиентного спуска в задаче линейной МНК регрессии 
    """

    def __init__(self, samples: pd.DataFrame, targets: pd.DataFrame,
                 learning_rate: float = 1e-3, threshold = 1e-6, copy: bool = True):
        """
        self.samples - матрица признаков
        self.targets - вектор таргетов
        self.beta - вектор из изначальными весами модели == коэффициентами бета (состоит из единиц)
        self.learning_rate - параметр *learning_rate* для корректировки нормы градиента
        self.threshold - величина, меньше которой изменение в loss-функции означает остановку градиентного спуска
        iteration_loss_dict - словарь, который будет хранить номер итерации и соответствующую MSE
        copy: копирование матрицы признаков или создание изменения in-place
        """
        ### Your code is here
        self.samples = samples
        self.targets = targets.to_numpy()
        self.beta = np.ones(samples.shape[1])
        self.learning_rate = learning_rate
        self.threshold = threshold
        self.copy = copy
        self.iteration_loss_dict = {}
        
    def add_constant_feature(self):
        """
        Метод для создания константной фичи в матрице объектов samples
        Метод создает колонку с константным признаком (interсept) в матрице признаков.
        Hint: так как количество признаков увеличилось на одну, не забудьте дополнить вектор с изначальными весами модели!
        """
        ### Your code is here
        self.samples = np.concatenate([self.samples, np.ones(self.samples.shape[0])[..., np.newaxis]], axis=1)
        self.beta = np.concatenate([self.beta, np.ones(1)])
        
    def calculate_mse_loss(self) -> float:
        """
        Метод для расчета среднеквадратической ошибки
        
        :return: среднеквадратическая ошибка при текущих весах модели : float
        """
        ### Your code is here
        # beta.shape == (f,) & samples.shape == (n, f)
        # beta.reshape(-1, 1) == (f, 1)
        beta_reshaped = self.beta.reshape(-1, 1)
        loss = np.mean((np.dot(self.samples, beta_reshaped) - self.targets.reshape(-1, 1))**2)

        return loss

    def calculate_gradient(self) -> np.ndarray:
        """
        Метод для вычисления вектора-градиента
        Метод возвращает вектор-градиент, содержащий производные по каждому признаку.
        Сначала матрица признаков скалярно перемножается на вектор self.beta, и из каждой колонки
        полученной матрицы вычитается вектор таргетов. Затем полученная матрица скалярно умножается на матрицу признаков.
        Наконец, итоговая матрица умножается на 2 и усредняется по каждому признаку.
        
        :return: вектор-градиент, т.е. массив, содержащий соответствующее количество производных по каждой переменной : np.ndarray
        """
        ### Your code is here
        L = np.dot(self.samples, self.beta.T) - self.targets
        dQ = np.dot(L.T, self.samples) * 2 / self.samples.shape[0]
        return dQ
    
    
    def iteration(self):
        """
        Обновляем веса модели в соответствии с текущим вектором-градиентом
        """
        ### Your code is here
        self.beta = self.beta - self.learning_rate * self.calculate_gradient()
        
    def append_loss_dict(self, loss):
        if len(self.iteration_loss_dict) == 0:
            index_to_paste = 0
        else:
            index_to_paste = max(self.iteration_loss_dict.keys()) + 1
            
        self.iteration_loss_dict[index_to_paste] = loss
        print(f"Iteration: {index_to_paste} and current loss {loss}")
        
    def learn(self):
        """
        Итеративное обучение весов модели до срабатывания критерия останова
        Запись mse и номера итерации в iteration_loss_dict
        
        Описание алгоритма работы для изменения бет:
            Фиксируем текущие beta -> start_betas
            Делаем шаг градиентного спуска
            Записываем новые beta -> new_betas
            Пока |L(new_beta) - L(start_beta)| > threshold:
                Повторяем первые 3 шага
                
        Описание алгоритма работы для изменения функции потерь:
            Фиксируем текущие mse -> previous_mse
            Делаем шаг градиентного спуска
            Записываем новые mse -> next_mse
            Пока |(previous_mse) - (next_mse)| > threshold:
                Повторяем первые 3 шага
        """
        ### Your code is here
        start_betas = self.beta.copy()
        start_loss = self.calculate_mse_loss()
        self.append_loss_dict(start_loss)
        
        self.iteration()
        
        new_betas = self.beta.copy()
        new_loss = self.calculate_mse_loss()
        self.append_loss_dict(new_loss)
        
        while abs(new_loss - start_loss) > self.threshold and abs(np.linalg.norm(new_betas) - np.linalg.norm(start_betas)) > self.threshold:
            start_betas = self.beta.copy()
            start_loss = self.calculate_mse_loss()
            self.append_loss_dict(start_loss)
            
            self.iteration()
            
            new_betas = self.beta.copy()
            new_loss = self.calculate_mse_loss()
            self.append_loss_dict(new_loss)
          
          
if __name__ == "__main__":  
    data = pd.read_csv('1_lesson_4\\data.csv')
    
    ### Your code is here
    model = LinearRegression(fit_intercept=True)
    X = data.drop(columns=['target'])
    Y = data['target']

    model.fit(X,Y)
    
    GD = GradientDescentMse(samples=X, targets=Y)
    GD.add_constant_feature()
    GD.learn()
    print(GD.betas)