import torch.nn as nn
import torch.nn.functional as F


class FaceHRNet09V2ELU(nn.Module):
    def __init__(self, rgb):
        super(FaceHRNet09V2ELU, self).__init__()

        self.rgb = rgb

        self.ada_avg_pool2d = nn.AdaptiveAvgPool2d(output_size=(192, 128))

        conv_init_mean = 0
        conv_init_std = .1
        xavier_normal_gain = 1

        self.bn_input = nn.BatchNorm2d(3 if rgb else 1)
        nn.init.normal(self.bn_input.weight, conv_init_mean, conv_init_std)

        input_count = 1
        if self.rgb:
            input_count = 3

        output_count = 64  # int(32 * (1/0.9))
        self.conv_00 = nn.Conv2d(input_count, output_count, kernel_size=(15, 10), stride=1, padding=0)
        nn.init.xavier_normal(self.conv_00.weight, gain=xavier_normal_gain)
        self.max_pool2d_00 = nn.MaxPool2d(kernel_size=(15, 10), stride=(2, 2))
        self.bn_00 = nn.BatchNorm2d(output_count)
        nn.init.normal(self.bn_00.weight, conv_init_mean, conv_init_std)

        input_count = 64  # int(32 * (1/0.9))
        self.conv_01 = nn.Conv2d(input_count, output_count, kernel_size=(15, 10), stride=1, padding=0)
        nn.init.xavier_normal(self.conv_01.weight, gain=xavier_normal_gain)
        self.max_pool2d_01 = nn.MaxPool2d(kernel_size=(15, 10), stride=(1, 1))
        self.bn_01 = nn.BatchNorm2d(output_count)
        nn.init.normal(self.bn_01.weight, conv_init_mean, conv_init_std)

        # self.conv_02 = nn.Conv2d(input_count, output_count, kernel_size=(3, 3), stride=1, padding=0)
        # nn.init.xavier_normal(self.conv_02.weight, gain=xavier_normal_gain)
        # self.bn_02 = nn.BatchNorm2d(output_count)
        # nn.init.normal(self.bn_02.weight, conv_init_mean, conv_init_std)

        output_count = 128  # int(64 * (1/0.85))
        self.conv_10 = nn.Conv2d(input_count, output_count, kernel_size=(15, 10), stride=1, padding=0)
        nn.init.xavier_normal(self.conv_10.weight, gain=xavier_normal_gain)
        self.max_pool2d_10 = nn.MaxPool2d(kernel_size=(15, 10), stride=(1, 1))
        self.bn_10 = nn.BatchNorm2d(output_count)
        nn.init.normal(self.bn_10.weight, conv_init_mean, conv_init_std)

        input_count = 128
        # self.conv_11 = nn.Conv2d(input_count, output_count, kernel_size=(3, 3), stride=1, padding=0)
        # nn.init.xavier_normal(self.conv_11.weight, gain=xavier_normal_gain)
        # self.bn_11 = nn.BatchNorm2d(output_count)
        # nn.init.normal(self.bn_11.weight, conv_init_mean, conv_init_std)

        # self.conv_12 = nn.Conv2d(input_count, output_count, kernel_size=(3, 3), stride=1, padding=0)
        # nn.init.xavier_normal(self.conv_12.weight, gain=xavier_normal_gain)
        # self.bn_12 = nn.BatchNorm2d(output_count)
        # nn.init.normal(self.bn_12.weight, conv_init_mean, conv_init_std)

        output_count = 128
        self.conv_20 = nn.Conv2d(input_count, output_count, kernel_size=(12, 10), stride=1, padding=0)
        nn.init.xavier_normal(self.conv_20.weight, gain=xavier_normal_gain)
        self.max_pool2d_20 = nn.MaxPool2d(kernel_size=(15, 10), stride=(1, 1))
        self.bn_20 = nn.BatchNorm2d(output_count)
        nn.init.normal(self.bn_20.weight, conv_init_mean, conv_init_std)

        # input_count = 128#int(128 * (1/0.8))
        # self.conv_21 = nn.Conv2d(input_count, output_count, kernel_size=(4, 4), stride=1, padding=0)
        # nn.init.xavier_normal(self.conv_21.weight, gain=xavier_normal_gain)
        # self.bn_21 = nn.BatchNorm2d(output_count)
        # nn.init.normal(self.bn_21.weight, conv_init_mean, conv_init_std)

        # self.conv_22 = nn.Conv2d(input_count, output_count, kernel_size=(4, 4), stride=1, padding=0)
        # nn.init.xavier_normal(self.conv_22.weight, gain=xavier_normal_gain)
        # self.bn_22 = nn.BatchNorm2d(output_count)
        # nn.init.normal(self.bn_22.weight, conv_init_mean, conv_init_std)

        # output_count = 2048#int(2048 * (1/0.7))
        # self.conv_30 = nn.Conv2d(input_count, output_count, kernel_size=(5, 5), stride=1, padding=0)
        # nn.init.xavier_normal(self.conv_30.weight, gain=xavier_normal_gain)
        # self.bn_30 = nn.BatchNorm2d(output_count)
        # nn.init.normal(self.bn_30.weight, conv_init_mean, conv_init_std)

        # input_count = 2048#int(2048 * (1/0.7))
        # self.conv_31 = nn.Conv2d(input_count, output_count, kernel_size=(3, 3), stride=1, padding=0)
        # nn.init.xavier_normal(self.conv_31.weight, gain=xavier_normal_gain)
        # self.bn_31 = nn.BatchNorm2d(output_count)
        # nn.init.normal(self.bn_31.weight, conv_init_mean, conv_init_std)

        # self.conv_32 = nn.Conv2d(input_count, output_count, kernel_size=(3, 3), stride=1, padding=0)
        # nn.init.xavier_normal(self.conv_32.weight, gain=xavier_normal_gain)
        # self.bn_32 = nn.BatchNorm2d(output_count)
        # nn.init.normal(self.bn_32.weight, conv_init_mean, conv_init_std)

        input_count = 128
        self.conv_last = nn.Conv2d(input_count, 1, kernel_size=1, stride=1, padding=0)
        nn.init.xavier_normal(self.conv_last.weight, gain=xavier_normal_gain)



    def forward(self, x):
        nonlin = F.elu

        x = self.ada_avg_pool2d(x)

        x = self.bn_input(x)

        # x = nonlin(self.bn_00(self.conv_00(F.dropout(x, p=0.0, training=self.training))))
        x = nonlin(self.bn_00(self.max_pool2d_00(self.conv_00(F.dropout2d(x, p=0.0, training=self.training)))))
        x = nonlin(self.bn_01(self.max_pool2d_01(self.conv_01(F.dropout(x, p=0.0, training=self.training)))))
        x = nonlin(self.bn_10(self.max_pool2d_10(self.conv_10(F.dropout(x, p=0.0, training=self.training)))))
        # x = nonlin(self.bn_11(self.conv_11(F.dropout(x, p=0.0, training=self.training))))
        x = nonlin(self.bn_20(self.max_pool2d_20(self.conv_20(F.dropout2d(x, p=0.2, training=self.training)))))
        # x = nonlin(self.bn_21(self.conv_21(F.dropout(x, p=0.0, training=self.training))))
        # x = nonlin(self.bn_30(self.conv_30(F.dropout(x, p=0.0, training=self.training))))
        # x = nonlin(self.bn_31(self.conv_31(F.dropout(x, p=0.0, training=self.training))))

        x = self.conv_last(F.dropout(x, p=0.5, training=self.training))

        if sum(x.size()[1:]) > x.dim() - 1:
            print(x.size())
            raise ValueError('Check your network idiot!')

        return x
