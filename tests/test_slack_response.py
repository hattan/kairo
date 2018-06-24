import sys
sys.path.append("kairo")
from slack_response import *


def test_attachment_sets_pretext():
    # arrange
    pre_text = "preprepre"

    # act
    text, attachment = SlackResponse.attachment(pretext = pre_text)

    # assert
    assert attachment == [{'pretext' : pre_text}]

def test_attachment_sets_text():
    # arrange
    t = "ttt"

    # act
    text, attachment = SlackResponse.attachment(text = t)

    # assert
    assert attachment == [{'text' : t}]

def test_attachment_sets_author_name():
    # arrange
    a = "bob"

    # act
    text, attachment = SlackResponse.attachment(author_name = a)

    # assert
    assert attachment == [{'author_name' : a}]

def test_attachment_sets_author_link():
    # arrange
    l = "foo.com"

    # act
    text, attachment = SlackResponse.attachment(author_link = l)

    # assert
    assert attachment == [{'author_link' : l}]

def test_attachment_returns_text_as_None():
    # act
    text, attachment = SlackResponse.attachment("test")

    # assert
    assert text is None

def test_attachment_can_set_multiple_props():
    # arrange
    a = "bob"
    l = "foo.com"
    pre_text = "preprepre"

    # act
    text, attachment = SlackResponse.attachment(pretext=pre_text,author_link=l,author_name=a)

    # assert
    assert attachment == [{'pretext' : pre_text,'author_name' : a, 'author_link' : l}]